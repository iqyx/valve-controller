#include <stdint.h>
#include <string.h>

#include "ch.h"
#include "hal.h"

#include "lwip/opt.h"
#include "lwip/def.h"
#include "lwip/pbuf.h"
#include "lwip/tcpip.h"

#include "discovery.h"


discovery_ret_t discovery_init(Discovery *self) {
	if (self == NULL) {
		return DISCOVERY_FAILED;
	}

	memset(self, 0, sizeof(Discovery));

	self->pcb = udp_new();
	if (self->pcb == NULL) {
		return DISCOVERY_FAILED;
	}

	udp_connect(self->pcb, IP_ADDR_BROADCAST, 5001);

	return DISCOVERY_OK;
}


discovery_ret_t discovery_free(Discovery *self) {
	if (self == NULL) {
		return DISCOVERY_FAILED;
	}

	return DISCOVERY_OK;
}


discovery_ret_t discovery_set_mac(Discovery *self, const uint8_t mac[6]) {
	if (self == NULL) {
		return DISCOVERY_FAILED;
	}

	memcpy(self->mac, mac, 6);

	return DISCOVERY_OK;
}


discovery_ret_t discovery_set_ip(Discovery *self, const uint8_t ip[4]) {
	if (self == NULL) {
		return DISCOVERY_FAILED;
	}

	memcpy(self->ip, ip, 4);

	return DISCOVERY_OK;
}


discovery_ret_t discovery_send_broadcast(Discovery *self) {
	if (self == NULL) {
		return DISCOVERY_FAILED;
	}
	self->interval++;
	if (self->interval < DISCOVERY_INTERVAL) {
		return DISCOVERY_OK;
	}
	self->interval = 0;

	/* "vc" + ip (4) + mac (6) */
	uint8_t payload[12];
	memcpy(payload, "vc", 2);
	memcpy(payload + 2, self->ip, 4);
	memcpy(payload + 6, self->mac, 6);

	struct pbuf *pb = pbuf_alloc(PBUF_TRANSPORT, 12, PBUF_REF);
	pb->payload = payload;
	udp_send(self->pcb, pb);
	pbuf_free(pb);

	return DISCOVERY_OK;
}



