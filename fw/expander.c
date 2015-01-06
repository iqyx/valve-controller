#include "ch.h"
#include "hal.h"


#include "expander.h"

uint32_t e_ledg = 0, e_ledr = 0, e_valve = 0, e_state = 0;
static uint8_t e_ledgmap[8] = {1, 5, 14, 9, 6, 2, 9, 13};
static uint8_t e_ledrmap[8] = {0, 4, 15, 8, 7, 3, 8, 12};
static uint8_t e_valvemap[8] = {3, 7, 12, 11, 4, 0, 11, 15};
static uint8_t e_statemap[8] = {2, 6, 13, 10, 5, 1, 10, 14};


static const SPIConfig expcfg_a = {
	NULL,
	EXP_CS1PORT,
	EXP_CS1,
	SPI_CR1_BR_2 | SPI_CR1_BR_0,
};

static const SPIConfig expcfg_b = {
	NULL,
	EXP_CS2PORT,
	EXP_CS2,
	SPI_CR1_BR_2 | SPI_CR1_BR_0,
};


int expander_write_reg(const SPIConfig *port, int block, uint8_t addr, uint8_t reg, uint8_t data) {
	uint8_t txbuf[3];

	txbuf[0] = addr;
	txbuf[1] = reg;
	txbuf[2] = data;
	
	spiAcquireBus(port);
	if (block == 0) {
		spiStart(port, &expcfg_a);
	} else {
		spiStart(port, &expcfg_b);
	}

	spiSelect(port);
	spiSend(port, 3, txbuf);
	spiUnselect(port);

	spiReleaseBus(port);
}


int expander_update() {
	uint16_t reg_temp[8];
	int b, i;

	for (i = 0; i < 8; i++) {
		reg_temp[i] = 0xffff;
	}
	
	/* for each bit */
	for (b = 0; b < 32; b++) {
		int expander = b / 4;
		int mapindex = b % 8;

		if (e_ledr & (1 << b)) {
			reg_temp[expander] &= ~(1 << (e_ledrmap[mapindex]));
		}
		if (e_ledg & (1 << b)) {
			reg_temp[expander] &= ~(1 << (e_ledgmap[mapindex]));
		}
		if (!(e_valve & (1 << b))) {
			reg_temp[expander] &= ~(1 << (e_valvemap[mapindex]));
		}
	}

	/* update expander registers */
	for (i = 0; i < 4; i++) {
		expander_write_reg(EXP_SPI, 0, 0x40 + (i << 1), 0x15, reg_temp[i * 2] >> 8);
		expander_write_reg(EXP_SPI, 0, 0x40 + (i << 1), 0x14, reg_temp[i * 2] & 0xff);

		expander_write_reg(EXP_SPI, 1, 0x40 + (i << 1), 0x15, reg_temp[i * 2 + 1] >> 8);
		expander_write_reg(EXP_SPI, 1, 0x40 + (i << 1), 0x14, reg_temp[i * 2 + 1] & 0xff);
	}


}



int expander_init() {
	int i;

	palSetPad(GPIOA, 15);
	chThdSleepMilliseconds(2);
	palClearPad(GPIOA, 15);
	chThdSleepMilliseconds(10);
	palSetPad(GPIOA, 15);
	chThdSleepMilliseconds(2);

	for (i = 0; i < 8; i++) {
		expander_write_reg(EXP_SPI, 0, 0x40 + (i << 1), 0x0a, 0x28);
		expander_write_reg(EXP_SPI, 1, 0x40 + (i << 1), 0x0a, 0x28);

		expander_write_reg(EXP_SPI, 0, 0x40 + (i << 1), 0x00, 0x00);
		expander_write_reg(EXP_SPI, 1, 0x40 + (i << 1), 0x00, 0x00);

		expander_write_reg(EXP_SPI, 0, 0x40 + (i << 1), 0x01, 0x00);
		expander_write_reg(EXP_SPI, 1, 0x40 + (i << 1), 0x01, 0x00);
	}

	expander_update();

//	expander_write_reg(0x40, 0x12, 0x55);
//	expander_write_reg(0x40, 0x13, 0x55);

}

