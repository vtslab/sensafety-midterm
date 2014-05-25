/*
================================================================================
  (c) 2014 Strukton Embedded Solutions

  Project/Module: Sensafety Gateway

  Description: Configuration file

  Reference:

  Version Control
  	  $workfile: configuration.h
  	  $Revision:
  	  $Date: 02-05-2014
  	  Modtime:

================================================================================
 */

#ifndef CONFIGURATION_H_
#define CONFIGURATION_H_

#define _BSD_SOURCE 								//Define necessary for the function usleep.

/**	Standard header files	**/
#include <pthread.h> /* POSIX Thread definitions */
#include <stdio.h>   /* Standard input/output definitions */
#include <stdlib.h>  /* General library functions */
#include <string.h>  /* String function definitions */
#include <unistd.h>  /* UNIX standard function definitions */
#include <fcntl.h>   /* File control definitions */
#include <errno.h>   /* Error number definitions */
#include <termios.h> /* POSIX terminal control definitions */

/* MQTT Constants */
#define MQTT_SERVERADDRESS "tcp://localhost:1883" 	// Address of MQTT broker
#define MQTT_ILP_ID "1"								// Client ID of this client

/* Led driver constants */
#define LEDDRIVER_COMPORT 22 						// 22 for "/dev/ttyAMA0"	 see rs232.c
#define LEDDRIVER_BAUDRATE 9600 					// Baud rate
#define MAXLEDDRIVERVALUE 4096						// Max value to receive and send to Led drivers

/* Miscellaneous */
#define ERROR_TIMEOUT 1 							// Timeout time in seconds
#define ERROR_RETRYCOUNT 3 							// Number of retry in case of fail transfer
#define LEDDRIVERS 6 								// Number of LED drivers available. 1..n
#define SLOWDOWNTIME 100							// Slow down timer for breaking the program for a while

/** Constants	**/
#define SUCCESS 0
#define TRUE 1
#define FALSE 0

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


struct
{
	INT8U id;
	BOOLEAN newValue;
	INT16U value;
	pthread_mutex_t threadLock;
} G_stLedDriver[LEDDRIVERS];

#endif /* CONFIGURATION_H_ */
