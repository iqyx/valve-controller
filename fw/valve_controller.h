#include "ch.h"
#include "hal.h"
#include "switching_board.h"

#ifndef _VALVE_CONTROLLER_H_
#define _VALVE_CONTROLLER_H_


#define VC_SPI &SPID3
#define VC_CS1 11
#define VC_CS1PORT GPIOC
#define VC_CS2 12
#define VC_CS2PORT GPIOC

#define VC_STATE_VALID_AGE 20

struct valve_controller {

	uint32_t state_valve;
	uint32_t state_highlight;
	uint32_t state_age;

	SPIConfig spicfg_a;
	SPIConfig spicfg_b;

	Thread *vc_thread;
	Mutex update_mtx;

	struct switching_board brd[4];

};



int32_t vc_init(struct valve_controller *vc);
#define VC_INIT_OK 0
#define VC_INIT_FAILED -1

int32_t vc_free(struct valve_controller *vc);
#define VC_FREE_OK 0
#define VC_FREE_FAILED -1

int32_t vc_update(struct valve_controller *vc);
#define VC_UPDATE_OK 0
#define VC_UPDATE_FAILED -1

int32_t vc_is_stalled(struct valve_controller *vc);

int32_t vc_set_valves(struct valve_controller *vc, uint32_t valves);
#define VC_SET_VALVES_OK 0
#define VC_SET_VALVES_FAILED -1


#endif

