/*
================================================================================
  (c) 2014 Strukton Embedded Solutions

  Project/Module: toggle_led

  Description: Toggle of an led on the Raspberry PI

  Reference:

  Version Control
  	  $workfile: main.c
  	  $Revision:
  	  $Date: 08-04-2014
  	  Modtime:

================================================================================
 */

#ifndef TOGGLE_LED_H_
#define TOGGLE_LED_H_

#define _BSD_SOURCE //Define necessary for the function usleep.

/**	Standard header files	**/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <pthread.h>
#include <string.h>
#include <fcntl.h>			//Used for UART
#include <termios.h>		//Used for UART


/** Special header files	**/
#include "Bsp/Include/Bsp_GPIO/gpio_e.h"

/** Type definitions **/
typedef unsigned char BOOLEAN;
typedef unsigned char INT8U;
typedef signed char INT8S;
typedef unsigned int INT16U;
typedef signed int INT16S;
typedef unsigned long INT32U;
typedef signed long INT32S;
typedef float FP32;
typedef double FP64;

/** Constants	**/
#define BUTTON  22 		/* P1-22 */
#define LEDGREEN 23  	/* P1-16 */
#define LEDYELLOW 24 	/* P1-18 */
#define LEDRED 25 		/* P1-22 */

/** Global variables	**/
INT8U ledPinGreen = LEDGREEN;
INT8U ledPinYellow = LEDYELLOW;
INT8U ledPinRed = LEDRED;

typedef struct
{
	INT8U ledPin;
	char ledColor[100];
	INT16U intervalTime;
} G_stLed;

G_stLed G_stGreenLed;
G_stLed G_stYellowLed;
G_stLed G_stRedLed;

/** Function prototypes **/
static INT8U initializeLeds ();
static INT8U clearGpio ();
static void ledTicker(void *);

#endif /* TOGGLE_LED_H_ */
