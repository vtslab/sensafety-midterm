/*
 * MQTT.c
 *
 *  Created on: May 1, 2014
 *      Author: jeffrey
 */

#include "App/Source/SapDriver/SapDriver.h"


INT8U initSapComm(){
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

INT8U sendMsgToSap(char* payload, char* topicName){
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
