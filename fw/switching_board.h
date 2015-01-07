#include "ch.h"
#include "hal.h"
#include "mcp23s17.h"

#ifndef _SWITCHING_BOARD_H_
#define _SWITCHING_BOARD_H_

struct switching_board {
	uint8_t state_ledg;
	uint8_t state_ledr;
	uint8_t state_valve;

	struct mcp23s17 expa;
	struct mcp23s17 expb;
};




int32_t sb_init(struct switching_board *sb, SPIDriver *port, const SPIConfig *cfg_a, const SPIConfig *cfg_b, uint8_t addr);
#define SB_INIT_OK 0
#define SB_INIT_FAILED -1

int32_t sb_free(struct switching_board *sb);
#define SB_FREE_OK 0
#define SB_FREE_FAILED -1

int32_t sb_update(struct switching_board *sb);
#define SB_UPDATE_OK 0
#define SB_UPDATE_FAILED -1

int32_t sb_set_ledg(struct switching_board *sb, uint8_t ledg);
#define SB_SET_LEDG_OK 0
#define SB_SET_LEDG_FAILED -1

int32_t sb_set_ledr(struct switching_board *sb, uint8_t ledr);
#define SB_SET_LEDR_OK 0
#define SB_SET_LEDR_FAILED -1

int32_t sb_set_valve(struct switching_board *sb, uint8_t valve);
#define SB_SET_VALVE_OK 0
#define SB_SET_VALVE_FAILED -1


#endif



