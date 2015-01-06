#ifndef _EXPANDER_H_
#define _EXPANDER_H_


#define EXP_SPI &SPID3
#define EXP_CS1 11
#define EXP_CS1PORT GPIOC
#define EXP_CS2 12
#define EXP_CS2PORT GPIOC


#define EXP_LED_GREEN 1
#define EXP_LED_RED 2
#define EXP_LED_ON 4
#define EXP_LED_PFF 8
#define EXP_VALVE 16


extern uint32_t e_ledg, e_ledr, e_valve, e_state;


int expander_write_reg(const SPIConfig *port, int block, uint8_t addr, uint8_t reg, uint8_t data);
int expander_update();
int expander_init();



#endif

