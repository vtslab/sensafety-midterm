
/**	Standard header files	**/
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

/** Special header files	**/
#include "MQTTClient.h"

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

/* Global variables */
#define ADDRESS "tcp://192.168.1.2:1883"
#define CLIENTID "clientID-Jeffrey"
#define TOPIC "topic-Jeffrey"
#define PAYLOAD "Hello World by Jeffrey!"
#define QOS 1
#define TIMEOUT 10000L
volatile MQTTClient_deliveryToken deliveredtoken;

void delivered(void *context, MQTTClient_deliveryToken dt);
int msgarrvd(void *context, char *topicName, int topicLen, MQTTClient_message *message);
void connlost(void *context, char *cause);
int MQTT_thread(INT8U *P_threadID);
