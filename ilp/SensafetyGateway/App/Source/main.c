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
//#include "App/Source/LedDriver/LedDriver.h"
#include "Extern/Source/RS232/rs232.h"

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
BOOLEAN G_fMqttBrokerComm = FALSE;
BOOLEAN G_fLedDriverComm = FALSE;
pthread_mutex_t signalIO_mutex     = PTHREAD_MUTEX_INITIALIZER;

/** Function prototypes **/
//static void threadLedDriver(int *P_threadID);
static BOOLEAN equalArrays (const INT8U *P_p1, const INT8U *P_p2, size_t P_size2);

int main(int argc, char* argv[])
{
	//	INT8U rc;
	//	INT32U value = 1;

	/* Creating Threads */
	//	int t2 = 2; // Thread ID
	//	pthread_t thread2; // Thread identities
	//	pthread_create(&thread2, NULL, (void*) threadLedDriver, &t2);

	int threadID = 2;
	int *P_threadID;
	P_threadID = &threadID;

	printf("Thread[%d]:Led Driver: Begin of thread ..\n\r", *P_threadID );

	INT8S L_rc = 0; // Return code
	size_t L_size = 0;
	INT8U L_rgReqMsg[] = {'c','o','m','r','e','q'}; // message for communication request
	INT8U L_rgConfMsg[] = {'c','o','m','c','o','n','f'}; // message for communication confirmation
	INT8U L_buf[4096];
	BOOLEAN G_fSerialPortOpen = FALSE;
	BOOLEAN L_fCommWithLedDriver = FALSE;
	BOOLEAN L_cConfReceived = FALSE;
	struct timeval L_sTimeout;
	INT8U L_failingCount = 0;

	int fd = 0;
	fd_set readset;

	while(TRUE)
	{
		printf("Thread[%d]:Led Driver: Trying to make connection ..\n\r", *P_threadID );

		/* Set up connection with Led Driver */
		L_rc = RS232_OpenComport(COMPORT, BAUDRATE);

		if (L_rc != SUCCESS) // if failed then..
		{
			printf("Thread[%d]:Led Driver: Failed to connect to Led Driver, return code [%d]\n\r", *P_threadID , L_rc );
		} else // else success
		{
			printf("Thread[%d]:Led Driver: Connection with Led Driver\n\r", *P_threadID );
			G_fSerialPortOpen = TRUE;

			/* Function Select needs File Descriptor (fd) settings.
			 * 	Added RS232_GetFileDes function to rs232 library to get the fd
			 * 	Make a fd set with the fd integer
			 */
			fd = RS232_GetFileDes(COMPORT);
			FD_ZERO(&readset);
			FD_SET(fd, &readset);
		}
		while(G_fSerialPortOpen)
		{
			/* Timeout time */
			L_sTimeout.tv_sec = ERRORTIMEOUT;    // seconds

			/* Send live signal to Led Driver to check if its alive */
			L_size = (sizeof(L_rgReqMsg) / sizeof(L_rgReqMsg[0]));
			L_rc = RS232_SendBuf(COMPORT, L_rgReqMsg, L_size);

			if (L_rc != SUCCESS)
			{
				printf("Thread[%d]:Led Driver: Connection lost with Led Driver, return code [%d]\n", *P_threadID, L_rc );

			} else // if request message is send..
			{
				/*
				 * Wait a time until there is information to read from serial line
				 * When timeout create an error (readyForReading = 0)
				 * */
				L_rc = select(fd + 1, &readset, NULL, NULL, &L_sTimeout);

				if ( 0 >= L_rc) // if error or timeout..
				{
					L_failingCount++;
					if (RETRYCOUNT <= L_failingCount) // if failed to many times..
					{
						printf("Thread[%d]:Led Driver: re-setup serial port\n", *P_threadID);
						G_fSerialPortOpen = FALSE;
						L_failingCount = 0;
						break;
					}
					if(0 == L_rc)
					{
						L_fCommWithLedDriver = FALSE;
						printf("Thread[%d]:Led Driver: Not alive, retrying %d/%d..\n", *P_threadID, L_failingCount, RETRYCOUNT);
					}else
					{
						printf("receiveMsgFromLedDriver: Error receiving message\n");
					}

				} else // if ready for reading file..
				{
					/* reset failing count */
					L_failingCount = 0;

					/* Read serial line */
					L_size = (sizeof(L_buf) / sizeof(L_buf[0]));
					L_rc = RS232_PollComport(COMPORT, L_buf, L_size);

					if (L_rc != SUCCESS)
					{
						printf("Thread[%d]:Led Driver: Failed to receive message from Led Driver, return code [%d]\n", *P_threadID, L_rc );
						L_fCommWithLedDriver = FALSE;

					} else // if received characters..
					{
						/* Check if received message is as expected */
						L_size = (sizeof(L_rgConfMsg) / sizeof(L_rgConfMsg[0]));
						L_cConfReceived = equalArrays(L_buf, L_rgConfMsg, L_size);

						if (!L_cConfReceived) // not right or no confirmation code received
						{
							L_fCommWithLedDriver = FALSE;
							printf("Thread[%d]: Expected [%s] message from Led Driver but got [%s]\n", *P_threadID, L_rgConfMsg , L_buf );
							printf("Thread[%d]:Led Driver: Led Driver communication not alive\n", *P_threadID );
						} else // if right confirmation code is received..
						{
							L_fCommWithLedDriver = TRUE;
							printf("Thread[%d]:Led Driver: Led Driver communication alive\n", *P_threadID );
						}
					}
				}
			}
			/* Clear buffer */
			L_size = (sizeof(L_buf) / sizeof(L_buf[0]));
			memset(L_buf, 0, L_size);

			/* Interval time for checking if alive */
			usleep(1000 * 1000); // 1 sec..

		}
		/* Close COM port */
		RS232_CloseComport(COMPORT);

		/* Interval time for trying to make an connection */
		usleep(500 * 1000); // 500 ms..
	}
}

/* Convert value to char */
/* Send msg to MQTT Broker */
/*
		int size;
		size = sizeof(value);
		char str[size];
		sprintf(str, "%lu", value);

		rc = sendMsgToMqttBroker(&str[0], "sg1");
		if (rc != SUCCESS)
		{
			printf("Failed to send value to MQTT Broker, MQTT return code [%d]\n", rc);
		}
 */

/* Debug info*/
//printf("Message [%lu] send to Lamp Driver to MQTT Broker\n", value);

/* Increment value and sleep for a while.. */
//value++;
//usleep(500 * 1000);



//}

static BOOLEAN equalArrays (const INT8U *P_p1, const INT8U *P_p2, size_t P_size2)
{
	INT8U i;
	BOOLEAN rc = TRUE;

	for(i = 0; i < P_size2; i++)
	{
		if (P_p1[i] != P_p2[i])
		{
			rc = FALSE;
			break;
		}
	}

	return(rc);
}

/*******************************************************************************
 * Function:		threadLampDriverComm
 * Parameters(s):	Thread ID number
 * Returns:
 * Description:		Thread function to initialize and keeping life communication with Lamp Driver
 * 					and keeping this alive
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
//static void threadLedDriver(int *P_threadID)
//{
//	printf("Thread[%d]:Led Driver: Begin of thread ..\n\r", *P_threadID );
//
//	int rc; // Return code
//	char L_cReqMsg[] = "comreq"; // message for communication request
//	char L_cConfMsg[] = "comconf"; // message for communication confirmation
//	char buf[256];
//	BOOLEAN L_fCommWithLedDriver = FALSE;
//
//	while(TRUE)
//	{
//		printf("Thread[%d]:Led Driver: Trying to make connection ..\n\r", *P_threadID );
//		G_fLedDriverComm = FALSE;
//		/* Set up connection with Led Driver */
//		rc = setupLedDriverComm(SERIALDEVICE, SERIALBAUDRATE);
//		if (rc != SUCCESS) // if failed then..
//		{
//			printf("Thread[%d]:Led Driver: Failed to connect to Led Driver@%s, return code [%d]\n\r", *P_threadID, SERIALDEVICE , rc );
//			L_fCommWithLedDriver = FALSE;
//		} else // else success
//		{
//			printf("Thread[%d]:Led Driver: Connection with Led Driver@%s\n\r", *P_threadID, SERIALDEVICE );
//			L_fCommWithLedDriver = TRUE;
//		}
//		while(L_fCommWithLedDriver)
//		{
//			printf("Thread[%d]:Led Driver: There is communication..\n\r", *P_threadID );
//
//			/* Send live signal to Led Driver to check if its alive */
//			rc = sendMsgtoLedDriver(L_cReqMsg);
//			if (rc != SUCCESS)
//			{
//				printf("Thread[%d]:Led Driver: Connection lost with Led Driver, return code [%d]\n", *P_threadID, rc );
//				L_fCommWithLedDriver = FALSE;
//			} else // if request message is send..
//			{
//				rc = receiveMsgFromLedDriver(buf, sizeof(buf));
//				if (rc != SUCCESS)
//				{
//					printf("Thread[%d]:Led Driver: Failed to receive message from Led Driver, return code [%d]\n", *P_threadID, rc );
//					L_fCommWithLedDriver = FALSE;
//				} else if (buf == L_cReqMsg) // if right confirmation code is received..
//				{
//					printf("Thread[%d]:Led Driver: Led Driver communication alive\n", *P_threadID );
//				} else // not right confirmation code received
//				{
//					printf("Thread[%d]: Expected [%s] message from Led Driver but got [%s]\n", *P_threadID, L_cConfMsg , buf );
//					L_fCommWithLedDriver = FALSE;
//				}
//			}
//			/* Interval time for checking if alive */
//			usleep(1000 * 1000); // 1 sec..
//
//		}
//		/* Interval time for trying to make an connection */
//		usleep(500 * 1000); // 500 ms..
//	}
//
//}

/*******************************************************************************
 * Function:		threadMqttBrokerComm
 * Parameters(s):	Thread ID number
 * Returns:
 * Description:		Thread function to initialize communication with MQTT Broker
 * 					and keeping this alive
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
//static void threadMqttBrokerComm(void * threadID)
//{
//	int rc;
//	char L_sMsg[256];
//	char *p_startMsg;
//	p_startMsg = &L_sMsg[0];
//
//	while(TRUE)
//	{
//		/* Set up connection with MQTT Broker */
//		rc = initMqttBrokerComm();
//		if (rc != SUCCESS) // if failed then..
//		{
//			printf("Failed to connect to MQTT Broker@%s, return code [%d]\n", ADDRESS , rc);
//			G_fMqttBrokerComm = FALSE;
//		} else // else success
//		{
//			printf("Connection with MQTT Broker@%s\n",ADDRESS );
//			G_fMqttBrokerComm = TRUE;
//		}
//
//
//		while(G_fMqttBrokerComm)
//		{
//			printf("Thread[%p] While loop in threadLampDriverComm\n\r", threadID );
//
//			/* Send 'H'(ello) to Lamp Driver */
//			rc = sendMsgtoLampDriver('H');
//			if (rc != SUCCESS)
//			{
//				printf("Connection lost with Lamp Driver, Lamp Driver return code [%d]\n", rc);
//				G_fLampDriverComm = FALSE;
//			} else // if success..
//			{
//				/* Wait for confirmation msg 'W'(orld) from Lam Driver*/
//				rc = receiveMsgFromLampDriver(*p_startMsg);
//				if (rc != SUCCESS)
//				{
//					printf("Failed to receive message from Lamp Driver, Lamp Driver return code [%d]\n", rc);
//					G_fLampDriverComm = FALSE;
//				} else if ('W' == L_sMsg[0])
//				{
//					printf("Thread[%p] Lamp Driver communication life\n\r", threadID );
//				} else
//				{
//					printf("Expected 'W' message from Lamp Driver but got [%s]\n", L_sMsg);
//					G_fLampDriverComm = FALSE;
//				}
//			}
//		}
//	}
//
//}
