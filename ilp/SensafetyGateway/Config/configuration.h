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

/* Constants */
#define MQTT_ADDRESS "tcp://192.168.1.2:1883" // Address of MQTT broker
#define MQTT_CLIENTID "ilpClient1"	// Client ID of this client
#define COMPORT 22 // 22 for "/dev/ttyAMA0"	 see rs232.c
#define BAUDRATE 9600 // // Baud rate
#define ERRORTIMEOUT 1 // Timeout time in seconds
#define RETRYCOUNT 3 // Number of retry in case of fail transfer
#define LEDDRIVERS 6 // Number of LED drivers available

#endif /* CONFIGURATION_H_ */
