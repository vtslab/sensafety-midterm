/*
 ============================================================================
 Name        : Test-Project.c
 Author      : Jeffrey
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

#define MQTT_ILP_ID "1"

int main(void) {

	char topicName[] = "test1/met2/";
	char payload[] = "15987";
	size_t payloadlen = strlen(payload);
	size_t topicLen = strlen(topicName);
	INT8U i;
	INT8U L_receivedMsg[20];
	INT8U L_receivedTopic[topicLen];
	INT8U *L_pTopic;
	INT8U *L_pChar;
	INT8U L_topicLevelChar = '/';
	INT8U L_charBuf[100];
	INT8U L_topic [10] [20]; // 10 levels of topics and max 20 char topic name
	size_t L_size = 0;
	INT8U *L_pReceivedMsg;

	L_pReceivedMsg = (INT8U *) &payload;
	L_pTopic = (INT8U *) topicName;

	/* copy received message */
	for( i = 0 ; i < payloadlen ; i++ )
	{
		L_receivedMsg[i] = *L_pReceivedMsg;
		L_pReceivedMsg++;
	}
	/* Add '\0' to make a c string */
	L_receivedMsg[payloadlen] = '\0';

	/* Copy topic name */
	for( i = 0 ; i < topicLen ; i++ )
	{
		L_receivedTopic[i] = *L_pTopic;
		L_pTopic++;
	}
	/* Add '\0' to make a c string */
	L_receivedTopic[topicLen] = '\0';


	/* Decomposing the topic in levels */
	/* Expectation: {ilp, n , driver , n , value , n  */
	i = 0;
	while( 0 < strlen( (char *) L_receivedTopic))
	{
		/* Copy most left topic name in to array */
		L_size = strcspn ( (char *) &L_receivedTopic, (char *) &L_topicLevelChar );			// Get number of char until '/' or '\0'
		strncpy ( (char *) L_topic[i] , (char *) &L_receivedTopic , L_size); 				// Copy most left topic in to array
		L_topic[i][L_size] = '\0';															// Add terminating character

		/* Delete the  most left topic name */
		L_pChar = (INT8U *) strchr ( (char *) &L_receivedTopic, L_topicLevelChar); 			// Pointer to first '/' char
		if (NULL != L_pChar) 																// If char is found..
		{
			L_pChar++; 																		// Move pointer to position next to '/'
			strcpy ( (char *) &L_charBuf , (char *) L_pChar );								// Copy after '/' into buffer
			strcpy ( (char *) &L_receivedTopic, (char *) L_charBuf);						// Copy buffer back in to message
		}else 																				// Last message
		{
			L_receivedTopic[0] = '\0';														// Clear string because everyting is copied to array
		}
		i++;
	}
	/* Check if the right topics are delivered */
	if (0 == strcmp ( (char *) L_topic[0] , "ilp" ))
	{
		printf("ilp: [%s]\n", L_topic[0] );

		if (0 == strcmp ( (char *) L_topic[1] , MQTT_ILP_ID ))
		{
			printf("ilp nr: [%s]\n", L_topic[1] );

			if (0 == strcmp ( (char *) L_topic[2] , "driver" ))
			{
				printf("Driver: [%s]\n", L_topic[2] );

				if (0 <= atoi ( (char *) L_topic[3]))
				{
					printf("Driver nr: [%s]\n", L_topic[3] );

					if (0 == strcmp ( (char *) L_topic[4] , "value" ))
					{
						printf("Value: [%s]\n", L_topic[4] );

						if (0 <= atoi ( (char *) L_receivedMsg))
						{
							printf("Value nr: [%s]\n", L_receivedMsg );

						}
					}
				}
			}
		}
	}

	puts("!!!Hello World!!!"); /* prints !!!Hello World!!! */
	return EXIT_SUCCESS;
}

