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

#ifndef LAMPDRIVER_H_
#define LAMPDRIVER_H_

#define _BSD_SOURCE //Define necessary for the function usleep.

/**	Standard header files	**/
#include <pthread.h> /* POSIX Thread definitions */
#include <stdio.h>   /* Standard input/output definitions */
#include <stdlib.h>  /* General library functions */
#include <string.h>  /* String function definitions */
#include <unistd.h>  /* UNIX standard function definitions */
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <termios.h> /* POSIX terminal control definitions */

/** Type definitions **/
typedef unsigned char INT8U;

/** Constants	**/
#define _POSIX_SOURCE 1 /* POSIX compliant source */

/** Global variables	**/
int uart0_fd; // File descriptor for UART0

/** Function prototypes	**/
INT8U initLampDriverComm(const char *, const char);
void CloseUart();
void sendStringOverUart(char *);
void clearScreen();
void blinkScreen();
void clearLine();
void cursorToLine (INT8U);
void cursorToColumn (INT8U);
void terminalReset();
void readLine(char *);

#endif /* LAMPDRIVER_H_ */
