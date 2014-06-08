
#ifndef MQTTBROKER_H
#define MQTTBROKER_H

/** Special header files	**/
#include "MQTTClient.h"
#include "Config/Configuration_E.h"
#include "App/Include/GlobalDefs_E.h"
#include "libxml/parser.h"

/* Global variables */
#define PAYLOAD "2045"
#define QOS 1
#define TIMEOUT 10000L
volatile MQTTClient_deliveryToken deliveredtoken;

typedef struct
{
	INT8U id;
	BOOLEAN newValue;
	INT16U value;
	pthread_mutex_t threadLock;
} ST_MQTTmsgQueue;

ST_MQTTmsgQueue G_stMQTTmsgQueue[LEDDRIVERS];

// Struct declaration and init for thread attributes
struct MQTT_threadData
{
	INT8U threadID;
	INT8U address[100];
	INT8U clientID;
};


/** Function prototypes **/
void MQTT_thread(void *P_stMQTT_threadPar);
static INT8U MQTT_setupConnection( MQTTClient *P_client , MQTTClient_connectOptions *P_conn_opts , const INT8U *P_threadID);
void MQTT_thread_delivered(void *context, MQTTClient_deliveryToken dt);
int MQTT_thread_msgarrvd(void *context, char *topicName, int topicLen, MQTTClient_message *message);
void MQTT_thread_connlost(void *context, char *cause);
static void MQTT_init();
static INT8U MQTT_subscribeTopics(MQTTClient *P_client ,const INT8U *P_threadID);

#endif /* MQTTBROKER_H */
