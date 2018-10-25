#include <stdint.h>
#include <string.h>

#include "ch.h"
#include "hal.h"

#include "lwip/opt.h"
#include "lwip/def.h"
#include "lwip/pbuf.h"
#include "lwip/tcpip.h"

#pragma once

#define DISCOVERY_PORT 5001
#define DISCOVERY_INTERVAL 10

typedef enum {
	DISCOVERY_OK,
	DISCOVERY_FAILED,
} discovery_ret_t;

typedef struct {
	uint8_t mac[6];
	uint8_t ip[4];
	uint32_t interval;

	struct udp_pcb *pcb;
} Discovery;


discovery_ret_t discovery_init(Discovery *self);
discovery_ret_t discovery_free(Discovery *self);
discovery_ret_t discovery_set_mac(Discovery *self, const uint8_t mac[6]);
discovery_ret_t discovery_set_ip(Discovery *self, const uint8_t ip[4]);
discovery_ret_t discovery_send_broadcast(Discovery *self);
