#include "ch.h"
#include "hal.h"

#include "lwip/opt.h"
#include "lwip/def.h"
#include "lwip/pbuf.h"
#include <lwip/tcpip.h>

#include "valve_controller.h"
#include "switching_board.h"


static msg_t vc_update_thread(void *arg) {

	struct valve_controller *vc = (struct valve_controller *)arg;
	chRegSetThreadName("vc_update");

	while (chThdShouldTerminate() == 0) {
		vc->state_age++;
		vc_update(vc);
		chThdSleepMilliseconds(250);
	}

	return 0;
}


static void vc_udp_recv(void *arg, struct udp_pcb *pcb, struct pbuf *p, struct ip_addr *addr, u16_t port) {

	(void)pcb;
	(void)addr;
	(void)port;

	struct valve_controller *vc = (struct valve_controller *)arg;
	if (p != NULL) {
		if (p->len == 5) {
			uint8_t *payload = (uint8_t *)(p->payload);
			uint32_t data =
				payload[1] << 24 |
				payload[2] << 16 |
				payload[3] <<  8 |
				payload[4];
			if (payload[0] == 'v') {
				vc_set_valves(vc, data);
			}
			if (payload[0] == 'h') {
				vc_set_highlight(vc, data);
			}
		}

		pbuf_free(p);
	}
}

int32_t vc_init(struct valve_controller *vc) {
	if (vc == NULL) {
		return VC_INIT_FAILED;
	}

	vc->state_valve = 0;
	vc->state_highlight = 0;
	vc->state_age = VC_STATE_VALID_AGE;
	chMtxInit(&vc->update_mtx);

	/* Dafuq? */
	palSetPad(GPIOA, 15);
	chThdSleepMilliseconds(2);
	palClearPad(GPIOA, 15);
	chThdSleepMilliseconds(10);
	palSetPad(GPIOA, 15);
	chThdSleepMilliseconds(2);

	/* Make SPI configuration for switching boards. */
	vc->spicfg_a = (SPIConfig){
		NULL,
		VC_CS1PORT,
		VC_CS1,
		SPI_CR1_BR_2 | SPI_CR1_BR_0,
	};
	vc->spicfg_b = (SPIConfig){
		NULL,
		VC_CS2PORT,
		VC_CS2,
		SPI_CR1_BR_2 | SPI_CR1_BR_0,
	};

	/* AInitialize all four switching boards. */
	for (uint8_t i = 0; i < 4; i++) {
		if (sb_init(&(vc->brd[i]), &SPID3, &vc->spicfg_a, &vc->spicfg_b, i) != SB_INIT_OK) {
			return VC_INIT_FAILED;
		}
	}

	if (vc_update(vc) != VC_UPDATE_OK) {
		return VC_INIT_FAILED;
	}

	vc->vc_thread = chThdCreateFromHeap(NULL, THD_WA_SIZE(128), NORMALPRIO, (tfunc_t)vc_update_thread, (void *)vc);
	if (vc->vc_thread == NULL) {
		return VC_INIT_FAILED;
	}

	/* Setup UDP server */
	struct udp_pcb *pcb = udp_new();
	if (pcb == NULL) {
		return VC_INIT_FAILED;
	}
	if (udp_bind(pcb, IP_ADDR_ANY, VC_UDP_PORT) != ERR_OK) {
		return VC_INIT_FAILED;
	}
	udp_recv(pcb, vc_udp_recv, (void *)vc);

	return VC_INIT_OK;
}


int32_t vc_free(struct valve_controller *vc) {
	if (vc == NULL) {
		return VC_FREE_FAILED;
	}

	chThdTerminate(vc->vc_thread);
	chThdWait(vc->vc_thread);
	vc->vc_thread = NULL;

	return VC_FREE_OK;
}


int32_t vc_update(struct valve_controller *vc) {
	if (vc == NULL) {
		return VC_UPDATE_FAILED;
	}

	/* Update must be done with mutex locked as it can be called
	 * from multiple threads. */
	chMtxLock(&vc->update_mtx);
	for (uint8_t i = 0; i < 4; i++) {
		if (vc_is_stalled(vc)) {
			/* state is invalid. Yellow leds blinks for all opened valves.
			 * Green leds are lit according to higlight. Valves are closed. */
			sb_set_valve(&(vc->brd[i]), 0x0000);

			if (vc->state_age % 2) {
				sb_set_ledr(&(vc->brd[i]), (vc->state_valve >> (i * 8)) & 0xff);
				sb_set_ledg(&(vc->brd[i]), ((vc->state_valve | vc->state_highlight) >> (i * 8)) & 0xff);
			} else {
				sb_set_ledr(&(vc->brd[i]), 0x0000);
				sb_set_ledg(&(vc->brd[i]), (vc->state_highlight >> (i * 8)) & 0xff);
			}
		} else {
			/* State is still valid, set valves and leds. */
			sb_set_ledr(&(vc->brd[i]), (vc->state_valve >> (i * 8)) & 0xff);
			sb_set_ledg(&(vc->brd[i]), (vc->state_highlight >> (i * 8)) & 0xff);
			sb_set_valve(&(vc->brd[i]), (vc->state_valve >> (i * 8)) & 0xff);
		}
	}
	chMtxUnlock();

	return VC_UPDATE_OK;
}


int32_t vc_is_stalled(struct valve_controller *vc) {
	return !(vc->state_age <= VC_STATE_VALID_AGE);
}


int32_t vc_set_valves(struct valve_controller *vc, uint32_t valves) {
	if (vc == NULL) {
		return VC_SET_VALVES_FAILED;
	}

	vc->state_valve = valves;
	vc->state_age = 0;
	if (vc_update(vc) != VC_UPDATE_OK) {
		return VC_SET_VALVES_FAILED;
	}

	return VC_SET_VALVES_OK;
}


int32_t vc_set_highlight(struct valve_controller *vc, uint32_t highlight) {
	if (vc == NULL) {
		return VC_SET_HIGHLIGHT_FAILED;
	}

	vc->state_highlight = highlight;
	vc->state_age = 0;
	if (vc_update(vc) != VC_UPDATE_OK) {
		return VC_SET_HIGHLIGHT_FAILED;
	}

	return VC_SET_HIGHLIGHT_OK;
}

