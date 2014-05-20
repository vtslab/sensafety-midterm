#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "MQTTAsync.h"

#define ADDRESS "tcp://192.168.1.2:1883" // Address of MQTT broker
#define CLIENTID "ilpClient"	// Client ID of this client
#define TOPIC       "ilp/1/1/"
#define PAYLOAD     "Hello World!"
#define QOS         1
#define TIMEOUT     10000L

volatile MQTTAsync_token deliveredtoken;
int disc_finished = 0;
int subscribed = 0;
int finished = 0;

void connlost(void *context, char *cause);
int msgarrvd(void *context, char *topicName, int topicLen, MQTTAsync_message *message);
void onDisconnect(void* context, MQTTAsync_successData* response);
void onSubscribe(void* context, MQTTAsync_successData* response);
void onSubscribeFailure(void* context, MQTTAsync_failureData* response);
void onConnectFailure(void* context, MQTTAsync_failureData* response);
void onConnect(void* context, MQTTAsync_successData* response);
int MQTT_main();
