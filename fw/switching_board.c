#include "ch.h"
#include "hal.h"

#include "switching_board.h"
#include "mcp23s17.h"

uint8_t sb_ledgmap[8] = {1, 5, 14, 9, 6, 2, 9, 13};
uint8_t sb_ledrmap[8] = {0, 4, 15, 8, 7, 3, 8, 12};
uint8_t sb_valvemap[8] = {3, 7, 12, 11, 4, 0, 11, 15};
uint8_t sb_statemap[8] = {2, 6, 13, 10, 5, 1, 10, 14};

int32_t sb_init(struct switching_board *sb, SPIDriver *port, const SPIConfig *cfg_a, const SPIConfig *cfg_b, uint8_t addr) {
	if (sb == NULL || port == NULL || cfg_a == NULL || cfg_b == NULL) {
		return SB_INIT_FAILED;
	}

	mcp23s17_init(&(sb->expa), port, cfg_a, addr);
	mcp23s17_init(&(sb->expb), port, cfg_b, addr);

	sb->state_ledg = 0;
	sb->state_ledr = 0;
	sb->state_valve = 0;

	return SB_INIT_OK;
}


int32_t sb_free(struct switching_board *sb) {
	if (sb == NULL) {
		return SB_FREE_FAILED;
	}

	/* Nothing to do here. */

	return SB_FREE_OK;
}


int32_t sb_update(struct switching_board *sb) {
	if (sb == NULL) {
		return SB_UPDATE_FAILED;
	}

	uint16_t reg_temp[2] = {0xffff, 0xffff};
	for (uint8_t b = 0; b < 8; b++) {
		if (sb->state_ledg & (1 << b)) {
			reg_temp[b / 4] &= ~(1 << (sb_ledgmap[b]));
		}
		if (sb->state_ledr & (1 << b)) {
			reg_temp[b / 4] &= ~(1 << (sb_ledrmap[b]));
		}
		if (!(sb->state_valve & (1 << b))) {
			reg_temp[b / 4] &= ~(1 << (sb_valvemap[b]));
		}
	}

	/* Update expander registers. */
	mcp23s17_set_port(&(sb->expa), reg_temp[0]);
	mcp23s17_set_port(&(sb->expb), reg_temp[1]);

	return SB_UPDATE_OK;
}


int32_t sb_set_ledg(struct switching_board *sb, uint8_t ledg) {
	if (sb == NULL) {
		return SB_SET_LEDG_FAILED;
	}

	sb->state_ledg = ledg;
	if (sb_update(sb) != SB_UPDATE_OK) {
		return SB_SET_LEDG_FAILED;
	}

	return SB_SET_LEDG_OK;
}


int32_t sb_set_ledr(struct switching_board *sb, uint8_t ledr) {
	if (sb == NULL) {
		return SB_SET_LEDR_FAILED;
	}

	sb->state_ledr = ledr;
	if (sb_update(sb) != SB_UPDATE_OK) {
		return SB_SET_LEDR_FAILED;
	}

	return SB_SET_LEDR_OK;
}


int32_t sb_set_valve(struct switching_board *sb, uint8_t valve) {
	if (sb == NULL) {
		return SB_SET_VALVE_FAILED;
	}

	sb->state_valve = valve;
	if (sb_update(sb) != SB_UPDATE_OK) {
		return SB_SET_VALVE_FAILED;
	}

	return SB_SET_VALVE_OK;
}
