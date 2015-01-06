/*
    ChibiOS/RT - Copyright (C) 2006,2007,2008,2009,2010,
                 2011,2012 Giovanni Di Sirio.

    This file is part of ChibiOS/RT.

    ChibiOS/RT is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    ChibiOS/RT is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

                                      ---

    A special exception to the GPL can be applied should you wish to distribute
    a combined work that includes ChibiOS/RT, without being obliged to provide
    the source code for any proprietary components. See the file exception.txt
    for full details of how and when the exception can be applied.
*/

#ifndef _BOARD_H_
#define _BOARD_H_

/*
 * Setup for the STMicroelectronics STM3210C-EVAL evaluation board.
 */

/*
 * Board identifier.
 */
#define BOARD_ETHTEMP4_SIMPLE
#define BOARD_NAME              "valve_controller"

/*
 * Board frequencies.
 */
#define STM32_LSECLK            32768
#define STM32_HSECLK            16000000

/*
 * MCU type, supported types are defined in ./os/hal/platforms/hal_lld.h.
 */
#define STM32F10X_CL

/*
 * Ethernet PHY type.
 */
#define MII_KSZ8081RNA_ID	0x00221560
#define BOARD_PHY_ID            MII_KSZ8081RNA_ID
#define BOARD_PHY_RMII

/*
 * IO pins assignments.
 */

#define GPIOB_LED_STATUS	8

/*
 * I/O ports initial setup, this configuration is established soon after reset
 * in the initialization code.
 *
 * The digits have the following meaning:
 *   0 - Analog input.
 *   1 - Push Pull output 10MHz.
 *   2 - Push Pull output 2MHz.
 *   3 - Push Pull output 50MHz.
 *   4 - Digital input.
 *   5 - Open Drain output 10MHz.
 *   6 - Open Drain output 2MHz.
 *   7 - Open Drain output 50MHz.
 *   8 - Digital input with PullUp or PullDown resistor depending on ODR.
 *   9 - Alternate Push Pull output 10MHz.
 *   A - Alternate Push Pull output 2MHz.
 *   B - Alternate Push Pull output 50MHz.
 *   C - Reserved.
 *   D - Alternate Open Drain output 10MHz.
 *   E - Alternate Open Drain output 2MHz.
 *   F - Alternate Open Drain output 50MHz.
 * Please refer to the STM32 Reference Manual for details.
 */


#define VAL_GPIOACRL            0x48888f48
#define VAL_GPIOACRH            0x18888888
#define VAL_GPIOAODR            0xFFFFFFFF

#define VAL_GPIOBCRL            0xff989888
#define VAL_GPIOBCRH            0x88bbb482
#define VAL_GPIOBODR            0xFFFFFFFF

#define VAL_GPIOCCRL            0x884488b2
#define VAL_GPIOCCRH            0x88811888
#define VAL_GPIOCODR            0xFFFFFFFF

#define VAL_GPIODCRL            0x88888888
#define VAL_GPIODCRH            0x88888888
#define VAL_GPIODODR            0xFFFFFFFF

#define VAL_GPIOECRL            0x88888888
#define VAL_GPIOECRH            0x88888888
#define VAL_GPIOEODR            0xFFFFFFFF

#if !defined(_FROM_ASM_)
#ifdef __cplusplus
extern "C" {
#endif
  void boardInit(void);
#ifdef __cplusplus
}
#endif
#endif /* _FROM_ASM_ */

#endif /* _BOARD_H_ */
