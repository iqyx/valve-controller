#include "ch.h"
#include "hal.h"

#include "mcp23s17.h"


int32_t mcp23s17_init(struct mcp23s17 *mcp, SPIDriver *port, const SPIConfig *port_config, uint8_t addr) {
	if (mcp == NULL || port == NULL || port_config == NULL) {
		return MCP23S17_INIT_FAILED;
	}

	mcp->port = port;
	mcp->port_config = port_config;
	mcp->addr = addr;
	mcp->port_output = 0;

	mcp23s17_write_reg(mcp, 0x0a, 0x28);
	mcp23s17_write_reg(mcp, 0x00, 0x00);
	mcp23s17_write_reg(mcp, 0x01, 0x00);

	return MCP23S17_INIT_OK;
}


int32_t mcp23s17_free(struct mcp23s17 *mcp) {
	if (mcp == NULL) {
		return MCP23S17_FREE_FAILED;
	}

	/* Nothing to do here. */

	return MCP23S17_FREE_OK;
}


int32_t mcp23s17_write_reg(struct mcp23s17 *mcp, uint8_t reg, uint8_t data) {
	if (mcp == NULL) {
		return MCP23S17_WRITE_REG_FAILED;
	}

	uint8_t txbuf[3];

	txbuf[0] = 0x40 + ((mcp->addr & 0x03) << 1);
	txbuf[1] = reg;
	txbuf[2] = data;

	spiAcquireBus(mcp->port);
	spiStart(mcp->port, mcp->port_config);
	spiSelect(mcp->port);
	spiSend(mcp->port, 3, txbuf);
	spiUnselect(mcp->port);
	spiReleaseBus(mcp->port);

	return MCP23S17_WRITE_REG_OK;
}


int32_t mcp23s17_update(struct mcp23s17 *mcp) {
	if (mcp == NULL) {
		return MCP23S17_UPDATE_FAILED;
	}

	if ((mcp23s17_write_reg(mcp, 0x15, (uint8_t)(mcp->port_output >> 8)) != MCP23S17_WRITE_REG_OK) ||
	    (mcp23s17_write_reg(mcp, 0x14, (uint8_t)(mcp->port_output & 0xff)) != MCP23S17_WRITE_REG_OK)) {
		return MCP23S17_UPDATE_FAILED;
	}

	return MCP23S17_UPDATE_OK;
}


int32_t mcp23s17_set_pin(struct mcp23s17 *mcp, uint8_t pin) {
	if (mcp == NULL || pin > 15) {
		return MCP23S17_SET_PIN_FAILED;
	}

	mcp->port_output |= (1 << pin);
	if (mcp23s17_update(mcp) != MCP23S17_UPDATE_OK) {
		return MCP23S17_SET_PIN_FAILED;
	}

	return MCP23S17_SET_PIN_OK;
}


int32_t mcp23s17_clear_pin(struct mcp23s17 *mcp, uint8_t pin) {
	if (mcp == NULL || pin > 15) {
		return MCP23S17_CLEAR_PIN_FAILED;
	}

	mcp->port_output &= ~(1 << pin);
	if (mcp23s17_update(mcp) != MCP23S17_UPDATE_OK) {
		return MCP23S17_CLEAR_PIN_FAILED;
	}

	return MCP23S17_CLEAR_PIN_OK;
}


int32_t mcp23s17_set_port(struct mcp23s17 *mcp, uint16_t port) {
	if (mcp == NULL) {
		return MCP23S17_SET_PORT_FAILED;
	}

	mcp->port_output = port;
	if (mcp23s17_update(mcp) != MCP23S17_UPDATE_OK) {
		return MCP23S17_SET_PORT_FAILED;
	}

	return MCP23S17_SET_PORT_OK;

}

