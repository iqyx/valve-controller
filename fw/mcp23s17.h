#include "ch.h"
#include "hal.h"

#ifndef _MCP23S17_H_
#define _MCP23S17_H_


struct mcp23s17 {
	SPIDriver *port;
	const SPIConfig *port_config;
	uint8_t addr;

	uint16_t port_output;

};



int32_t mcp23s17_init(struct mcp23s17 *mcp, SPIDriver *port, const SPIConfig *port_config, uint8_t addr);
#define MCP23S17_INIT_OK 0
#define MCP23S17_INIT_FAILED -1

int32_t mcp23s17_free(struct mcp23s17 *mcp);
#define MCP23S17_FREE_OK 0
#define MCP23S17_FREE_FAILED -1

int32_t mcp23s17_write_reg(struct mcp23s17 *mcp, uint8_t reg, uint8_t data);
#define MCP23S17_WRITE_REG_OK 0
#define MCP23S17_WRITE_REG_FAILED -1

int32_t mcp23s17_update(struct mcp23s17 *mcp);
#define MCP23S17_UPDATE_OK 0
#define MCP23S17_UPDATE_FAILED -1

int32_t mcp23s17_set_pin(struct mcp23s17 *mcp, uint8_t pin);
#define MCP23S17_SET_PIN_OK 0
#define MCP23S17_SET_PIN_FAILED -1

int32_t mcp23s17_clear_pin(struct mcp23s17 *mcp, uint8_t pin);
#define MCP23S17_CLEAR_PIN_OK 0
#define MCP23S17_CLEAR_PIN_FAILED -1

int32_t mcp23s17_set_port(struct mcp23s17 *mcp, uint16_t port);
#define MCP23S17_SET_PORT_OK 0
#define MCP23S17_SET_PORT_FAILED -1


#endif


