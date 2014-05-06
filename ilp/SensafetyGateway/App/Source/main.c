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
#include "App/Source/MqttBroker/MqttBroker.h"
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

BOOLEAN G_fmqttBrokerComm = FALSE;
BOOLEAN G_flampDriverComm = FALSE;

/** Function prototypes **/

int main(int argc, char* argv[])
{
	INT8U rc;
	INT32U value = 1;

	/* Set up connection with Situation Awareness Portal */
	rc = initMqttBrokerComm();
	if (rc != SUCCESS) // if failed then..
	{
		printf("Failed to connect to MQTT Broker@%s, return code [%d]\n", ADDRESS , rc);
		G_fmqttBrokerComm = FALSE;
	} else // else success
	{
		printf("Connection with MQTT Broker@%s\n",ADDRESS );
		G_fmqttBrokerComm = TRUE;
	}

	/* Set up connection with Lamp Driver */
	rc = initLampDriverComm(SERIALDEVICE, SERIALBAUDRATE);
	if (rc != SUCCESS) // if failed then..
	{
		printf("Failed to connect to Lamp Driver@%s, return code [%d]\n", SERIALDEVICE , rc);
		G_flampDriverComm = FALSE;
	} else // else success
	{
		printf("Connection with Lamp Driver@%s\n",SERIALDEVICE );
		G_flampDriverComm = TRUE;
	}

	while(TRUE)
	{
		/* Convert value to char */
		/* Send msg to MQTT Broker */
		int size;
		size = sizeof(value);
		char str[size];
		sprintf(str, "%lu", value);

		rc = sendMsgToMqttBroker(&str[0], "sg1");
		if (rc != SUCCESS)
		{
			printf("Failed to send value to MQTT Broker, MQTT return code [%d]\n", rc);
		}

		/* Send msg to Lamp Driver */
		char buf[256];
		sprintf (buf, "Msg ID[%lu]from SG\n\r", value);
		rc = sendStringOverUart(buf);
		if (rc != SUCCESS)
		{
			printf("Failed to send value to Lamp Driver, Lamp driver return code [%d]\n", rc);
		}
		/* Debug info*/
		printf("Message [%lu] send to Lamp Driver to MQTT Broker\n", value);

		/* Increment value and sleep for a while.. */
		value++;
		usleep(500 * 1000);
	}

}
