/*
================================================================================
  (c) 2014 Strukton Embedded Solutions

  Project/Module: GPIO driver for embedded Linux

  Description: Functions for controlling GPIO in- and outputs

  Reference:

  Version Control
  	  $workfile: gpio_e.h
  	  $Revision:
  	  $Date: 08-04-2014
  	  Modtime:

================================================================================
 */

#ifndef GPIO_H_
#define GPIO_H_

/**	Standard header files	**/
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/** Constants	**/
#define IN  0
#define OUT 1
#define LOW  0
#define HIGH 1
#define BUFFER_MAX 3
#define DIRECTION_MAX 35
#define VALUE_MAX 30

/** Type definitions **/
typedef unsigned char INT8U;

/** Function prototypes	**/

extern INT8U toggleOutput(INT8U);

extern INT8U GPIOExport(INT8U);

extern INT8U GPIOUnexport(INT8U);

extern INT8U GPIODirection(INT8U, INT8U);

extern INT8U GPIORead(INT8U);

extern INT8U GPIOWrite(INT8U, INT8U);

#endif /* GPIO_H_ */
