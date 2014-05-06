/*
================================================================================
  (c) 2014 Strukton Embedded Solutions

  Project/Module: Sensafety Gateway

  Description: Situation Awareness Portal driver

  Reference:

  Version Control
  	  $workfile: SapDriver.c
  	  $Revision:
  	  $Date: 02-05-2014
  	  Modtime:

================================================================================
 */

#include "App/Source/MqttBroker/MqttBroker.h"

/*******************************************************************************
 * Function:		initSapComm
 * Parameters(s):
 * Returns:			Returns !0 on failure or '0' when OK
 * Description:		Function to initialize communication with Backend
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
INT8U initMqttBrokerComm(){
	int rc;

	MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
	conn_opts.keepAliveInterval = 20;
	conn_opts.cleansession = 1;

	MQTTClient_create(&client, ADDRESS, CLIENTID,
			MQTTCLIENT_PERSISTENCE_NONE, NULL);

	if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS)
	{
		printf("Failed to connect, return code %d\n", rc);
		return rc;
	}
	return rc;
}

/*******************************************************************************
 * Function:		sendMsgToSap
 * Parameters(s):
 * Returns:			Returns !0 on failure or '0' when OK
 * Description:		Function to send a message to Sitation Awareness Portal
 * Reference:
 * Global/static variables
 * 						Payload - the actual message as a char array / string
 * 						topicName - ..
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
INT8U sendMsgToMqttBroker(char* payload, char* topicName){
	int rc;

	MQTTClient_message pubmsg = MQTTClient_message_initializer;
	pubmsg.payload = payload;
	pubmsg.payloadlen = strlen(payload);
	pubmsg.qos = QOS;
	pubmsg.retained = 0;

	MQTTClient_publishMessage(client, topicName, &pubmsg, &token);
	printf("Waiting for up to %d seconds for publication of %s\n"
			"on topic %s for client with ClientID: %s\n",
			(int)(TIMEOUT/1000), payload, topicName, CLIENTID);
	rc = MQTTClient_waitForCompletion(client, token, TIMEOUT);

	printf("Message with delivery token %d delivered\n", token);

	return rc;
}
