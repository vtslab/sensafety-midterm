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

/* MQTT Constants */
#define MQTT_SERVERADDRESS "tcp://localhost:1883" 	// Address of MQTT broker
#define MQTT_ILP_ID "1"								// Client ID of this client

/* Led driver constants */
#define LEDDRIVER_COMPORT 22 						// 22 for "/dev/ttyAMA0"	 see rs232.c
#define LEDDRIVER_BAUDRATE 9600 					// Baud rate
#define MAXLEDDRIVERVALUE 4096						// Max value to receive and send to Led drivers

#endif /* CONFIGURATION_H_ */
