/*
 * GlobalDefs_E.h
 *
 *  Created on: Jun 6, 2014
 *      Author: jeffrey
 */

#ifndef GLOBALDEFS_E_H_
#define GLOBALDEFS_E_H_

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

/* Global variables */
struct
{
	INT8U id;
	BOOLEAN newValue;
	INT16U value;
	pthread_mutex_t threadLock;
} G_stLedDriver[LEDDRIVERS];

/* Global variables */
extern BOOLEAN G_fMQTTBrokerComm;
extern BOOLEAN G_fLedDriverComm;



#endif /* GLOBALDEFS_E_H_ */
