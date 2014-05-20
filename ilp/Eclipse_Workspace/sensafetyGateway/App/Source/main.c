/*
================================================================================
  (c) 2014 Strukton Embedded Solutions

  Project/Module: Sensafety Gateway

  Description: Sensafety gateway between the Lamp Driver and SAP

  Reference:

  Version Control
  	  $workfile: main.c
  	  $Revision:
  	  $Date: 08-04-2014
  	  Modtime:

================================================================================
 */

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

/** Special header files	**/
#include "App/Source/SapDriver/SapDriver.h"
#include "App/Source/LampDriver/LampDriver.h"

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
#define SUCCESS 0
#define TRUE 1
#define FALSE 0

const char modemDevice[] = "/dev/ttyAMA0";
const char baudRate = B9600;

/** Function prototypes **/

int main(int argc, char* argv[])
{
	INT8U rc;
	INT32U value = 1;

	/* Set up connection with Situation Awareness Portal */
	if ((rc = initSapComm()) != SUCCESS) // if failed then..
	{
		printf("Failed to connect to Situation Awareness Portal, return code [%d]\n", rc);
	} else // else success
	{
		printf("Connection with Situation Awareness Portal\n");
	}

	/* Set up connection with Lamp Driver */

	initLampDriverComm(modemDevice, baudRate);


	while(TRUE)
	{
		/* Convert value to char */
		int size;
		size = sizeof(value);
		char str[size];
		sprintf(str, "%lu", value);

		/* Send msg to SAP */
		if ((rc = sendMsgToSap(&str[0], "sg1")) != SUCCESS)
		{
			printf("Failed to send value, MQTT return code [%d]\n", rc);
		}

		/* Send msg to Lamp Driver */
		sendStringOverUart("Msg from SG\n\r");

		/* Debug info*/
		printf("Message [%d] send to Lamp Driver to SAP\n", value);

		/* Increment value and sleep for a while.. */
		value++;
		usleep(250 * 1000);
	}

}
