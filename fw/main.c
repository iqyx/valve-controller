#include "ch.h"
#include "hal.h"
#include "chprintf.h"

#include "lwipthread.h"
#include "lwip/opt.h"
#include "lwip/def.h"
#include "lwip/mem.h"
#include "lwip/pbuf.h"
#include "lwip/sys.h"
#include <lwip/stats.h>
#include <lwip/snmp.h>
#include <lwip/tcpip.h>
#include "netif/etharp.h"
#include "netif/ppp_oe.h"
#include <lwip/sockets.h>
#include <string.h>

#include "expander.h"

#define ID_BASE 0x1ffff7e8


static WORKING_AREA(waThread1, 128);
static msg_t Thread1(void *arg) {
	(void)arg;
	chRegSetThreadName("led");

	while (1) {
		chThdSleepMilliseconds(500);
		palClearPad(GPIOB, 8);

		chThdSleepMilliseconds(500);
		palSetPad(GPIOB, 8);
	}
	return 0;
}

int main(void) {

	halInit();
	chSysInit();

	chThdSleepMilliseconds(100);

	expander_init();

	chThdCreateStatic(waThread1, sizeof(waThread1), NORMALPRIO, Thread1, NULL);

	uint8_t mac_address[6] = {
		0x02,
		*(unsigned char *)(ID_BASE + 7),
		*(unsigned char *)(ID_BASE + 8),
		*(unsigned char *)(ID_BASE + 9),
		*(unsigned char *)(ID_BASE + 10),
		*(unsigned char *)(ID_BASE + 11)
	};
	struct lwipthread_opts default_ip = {
		.macaddress = mac_address,
		.address = 0x1400a8c0,
		.netmask = 0x00ffffff,
		.gateway = 0x0100a8c0
	};
	chThdCreateStatic(wa_lwip_thread, LWIP_THREAD_STACK_SIZE, NORMALPRIO + 1, lwip_thread, &default_ip);


	int last_link_status = 0;
	while (1) {

		int current_link_status = netif_is_link_up(netif_default);
		if (current_link_status != last_link_status) {
			if (current_link_status) {
				netifapi_dhcp_start(netif_default);
			} else {
				netifapi_dhcp_stop(netif_default);
			}
		}
		last_link_status = current_link_status;

		chThdSleepMilliseconds(100);
	}

	while (1) {

	}

}
