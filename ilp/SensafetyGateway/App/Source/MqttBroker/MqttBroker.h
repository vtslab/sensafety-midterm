/*
================================================================================
  (c) 2014 Strukton Embedded Solutions

  Project/Module: Sensafety Gateway

  Description: Situation Awareness Portal driver

  Reference:

  Version Control
  	  $workfile: SapDriver.h
  	  $Revision:
  	  $Date: 02-05-2014
  	  Modtime:

================================================================================
 */

#ifndef MQTTBROKER_H_
#define MQTTBROKER_H_

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
#include <MQTTClient.h>
#include "Config/configuration.h"

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

#define PAYLOAD     "Hello World!"
#define QOS         1
#define TIMEOUT     10000L

MQTTClient client;
MQTTClient_deliveryToken token;

INT8U initMqttBrokerComm();

INT8U sendMsgToMqttBroker(char* str, char* topic);


#endif /* MQTTBROKER_H_ */
