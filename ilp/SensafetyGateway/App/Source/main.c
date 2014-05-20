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

Toolchaine settings:

for Raspberry Pi:
C/C++ Build -> Setting -> Cross settings
Prefix: arm-linux-gnueabihf-
Path : /home/jeffrey/tools/rpi-toolchain/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian/bin
libmqttv3c.so
libmqttv3c.so
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
#include "Extern/Source/RS232/rs232.h"
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

/** Constants	**/
#define SUCCESS 0
#define TRUE 1
#define FALSE 0

/* Global variables */
BOOLEAN G_fMqttBrokerComm = FALSE;
BOOLEAN G_fLedDriverComm = FALSE;

pthread_mutex_t signalIO_mutex = PTHREAD_MUTEX_INITIALIZER;

struct
{
	INT8U id;
	BOOLEAN newValue;
	INT16U value;
	pthread_mutex_t threadLock;
} G_stLedDriver[LEDDRIVERS];

struct
{
	INT8U threadID;
	INT8U address[100];
	INT8U client[100];
} MQTT_threadData;

struct MQTT_threadData G_stMQTT_threadPar = {
		.threadID = 3,
		.address = MQTT_ADDRESS,
		.client = MQTT_CLIENTID
};

/** Function prototypes **/
static void ledDriver_thread(INT8U *P_threadID);
static void ledDriver_init();
static BOOLEAN equalArrays (const INT8U *P_p1, const INT8U *P_p2,const size_t *P_size2);
static INT8U ledDriver_newValue(const INT8U *P_threadID, INT8U *P_driverNr);
static INT8U ledDriver_msgSentAndConfirmed(	const INT8U *P_threadID,
		const INT8U *P_sendMsg,
		const INT8U *P_confMsg,
		const size_t *P_sizeSendMsg,
		const size_t *P_sizeConfMsg);
static BOOLEAN ledDriver_SerialPortIsOpen(const INT8U *P_threadID);
static BOOLEAN equalArrays (const INT8U *P_p1, const INT8U *P_p2, const size_t *P_size2);
static void ledDriver_convertValueToMsg( const INT16U *P_value, INT8U *P_msg);
static void ledDriver_convertMsgToValue( const INT8U *P_msg, INT16U *P_value);

int main(int argc, char* argv[])
{
	ledDriver_init();

	/* Creating Threads */
	INT8U t2 = 2; // Thread ID
	pthread_t thread2, thread3; // Thread identities
	pthread_create(&thread2, NULL, (void*) ledDriver_thread, &t2);
	pthread_create(&thread3, NULL, (void*) MQTT_thread, &G_stMQTT_threadPar);

	// Main thread goes to sleep until thread is terminated. in this case for ever
	pthread_join(thread2, NULL);
	pthread_join(thread3, NULL);

	return(EXIT_SUCCESS);

}


/*******************************************************************************
 * Function:		threadLedDriverComm
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
static void ledDriver_thread(INT8U *P_threadID)
{
	printf("Thread[%d]:Led Driver: Begin of thread ..\n\r", *P_threadID );

	INT8S L_rc = 0; // Return code
	size_t L_size1 = 0;
	size_t L_size2 = 0;
	INT8U L_rgComReqMsg[] = "comreq"; // message for communication request
	INT8U L_rgComConfMsg[] = "comconf"; // message for communication confirmation
	INT8U L_rgValConfMsg[] = "valconf"; // message for value confirmation
	INT8U L_driverNr = 0;
	INT8U L_value[3] = {'0','0','0'}; // 2 bytes for value (max 65536) and one for \0


	while(TRUE)
	{
		while(ledDriver_SerialPortIsOpen(P_threadID))
		{
			/* Interval time for sending live signal */
			usleep(1000 * 1000);

			L_size1 = (sizeof(L_rgComReqMsg) / sizeof(L_rgComReqMsg[0]));
			L_size2 = (sizeof(L_rgComConfMsg) / sizeof(L_rgComConfMsg[0]));
			L_rc = ledDriver_msgSentAndConfirmed(P_threadID, L_rgComReqMsg, L_rgComConfMsg, &L_size1, &L_size2);

			if (!L_rc) // Not succes..
			{
				printf("Thread[%d]:Led Driver: Not alive\n", *P_threadID );
				RS232_CloseComport(COMPORT);
				break;
			} else
			{
				printf("Thread[%d]:Led Driver: Alive\n", *P_threadID );
				while (0 < ledDriver_newValue(P_threadID, &L_driverNr))
				{
					/* Interval time for sending new value */
					usleep(100 * 1000);

					L_driverNr--; // -1 accessing right driver. 1..n to 0..n

					ledDriver_convertValueToMsg( &G_stLedDriver[L_driverNr].value, L_value);

					L_size1 = (sizeof(L_value) / sizeof(L_value[0]));
					L_size2 = (sizeof(L_rgValConfMsg) / sizeof(L_rgValConfMsg[0]));
					L_rc = ledDriver_msgSentAndConfirmed(P_threadID, L_value, L_rgValConfMsg, &L_size1, &L_size2);

					if (!L_rc) // Not succes..
					{
						printf("Thread[%d]:Led Driver: Failed to update value\n", *P_threadID );
						pthread_mutex_unlock(&G_stLedDriver[L_driverNr].threadLock); // unlock locked driver
						break;
					} else // if succes..
					{
						printf("Thread[%d]:Led Driver: Driver [%d] updated with value [%d]\n", *P_threadID,(G_stLedDriver[L_driverNr].id + 1), G_stLedDriver[L_driverNr].value - 1);
						pthread_mutex_unlock(&G_stLedDriver[L_driverNr].threadLock); // unlock locked driver
						G_stLedDriver[L_driverNr--].newValue = FALSE;
					}

				}
			}

		}
		/* Interval time for setting up serial port */
		usleep(60000 * 1000);
	}
}

/*******************************************************************************
 * Function:		ledDriver_msgSentAndConfirmed
 * Parameters(s):	-- Thread ID,
 * 					-- Message to send
 * 					-- Message for confirmation
 * 					-- Size of message to send in bytes
 * 					-- Size of message to receive in bytes
 * Returns:			TRUE or FALSE
 * Description:		This function send a message over the serial port and
 * 					expect a confirmation of the serial device
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	-- Retry n-times when failing, else error
 *******************************************************************************/
static INT8U ledDriver_msgSentAndConfirmed(
		const INT8U *P_threadID,
		const INT8U *P_sendMsg,
		const INT8U *P_confMsg,
		const size_t *P_sizeSendMsg,
		const size_t *P_sizeConfMsg)
{
	BOOLEAN L_fReceivedConf = FALSE;
	INT8U L_rc = 0;
	INT8U L_buf[4096];
	size_t L_sizeBuf = 0;
	BOOLEAN L_cConfReceived = FALSE;
	struct timeval L_sTimeout;
	INT8U L_failingCount = 0;
	int fd = 0;
	fd_set readset;

	while (FALSE == L_fReceivedConf)
	{
		/* Send message to Led Driver */
		L_rc = RS232_SendBuf(COMPORT, P_sendMsg, *P_sizeSendMsg);

		if (L_rc != SUCCESS)
		{
			printf("Thread[%d]:Led Driver: Connection lost, return code [%d]\n", *P_threadID, L_rc );

		} else // if request message is send..
		{
			/* Timeout time */
			L_sTimeout.tv_sec = ERRORTIMEOUT;

			/* Function Select needs File Descriptor (fd) settings.
			 * 	Added RS232_GetFileDes function to rs232 library to get the fd
			 * 	Make a fd set with the fd integer
			 */
			fd = RS232_GetFileDes(COMPORT);
			FD_ZERO(&readset);
			FD_SET(fd, &readset);

			/*
			 * Wait a time until there is information to read from serial line
			 * When timeout create an error
			 * */
			L_rc = select(fd + 1, &readset, NULL, NULL, &L_sTimeout);


			if ( 0 >= L_rc) // if error or timeout..
			{
				L_failingCount++;

				if (RETRYCOUNT <= L_failingCount) // if failed to many times..
				{
					printf("Thread[%d]:Led Driver: Sending massage failed\n", *P_threadID);
					L_failingCount = 0;
					break;
				}

				printf("Thread[%d]:Led Driver: Timeout receiving confirmation message, retrying %d/%d..\n", *P_threadID, L_failingCount, RETRYCOUNT);

			} else // if ready for reading file..
			{
				/* reset failing count */
				L_failingCount = 0;

				/* Read serial line */
				L_sizeBuf = (sizeof(L_buf) / sizeof(L_buf[0]));
				L_rc = RS232_PollComport(COMPORT, L_buf, L_sizeBuf);

				if (L_rc != SUCCESS)
				{
					printf("Thread[%d]:Led Driver: Failed to receive message, return code [%d]\n", *P_threadID, L_rc );
					break;

				} else // if received characters..
				{
					/* Check if received message is as expected */
					L_cConfReceived = equalArrays(L_buf, P_confMsg, P_sizeConfMsg);

					if (!L_cConfReceived) // not right or no confirmation code received
					{
						printf("Thread[%d]: Expected [%s] message from Led Driver but got [%s]\n", *P_threadID, P_confMsg , L_buf );
					} else // if right confirmation code is received..
					{
						L_fReceivedConf = TRUE;
					}
				}
			}
		}
	}
	return(L_fReceivedConf);
}

/*******************************************************************************
 * Function:		ledDriver_SerialPortIsOpen
 * Parameters(s):
 * Returns:			TRUE or FALSE
 * Description:		This function opens the serial port for communicating
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *******************************************************************************/
static BOOLEAN ledDriver_SerialPortIsOpen(const INT8U *P_threadID)
{
	BOOLEAN L_fSerialPortOpen = FALSE;
	INT8U L_rc = 0;
	INT8U L_failingCount = 0;

	while(FALSE == L_fSerialPortOpen)
	{
		/* Set up connection with Led Driver */
		L_rc = RS232_OpenComport(COMPORT, BAUDRATE);

		if (L_rc != SUCCESS) // if failed then..
		{
			L_failingCount++;

			if (RETRYCOUNT <= L_failingCount) // if failed to many times..
			{
				printf("Thread[%d]:Led Driver: Failed to setup Serial port. Admin rights on port?\n", *P_threadID);
				L_failingCount = 0;

				/* Close COM port */
				RS232_CloseComport(COMPORT);

				break;
			}

			printf("Thread[%d]:Led Driver: Failed to setup serial port, retrying %d/%d..\n\r", *P_threadID , L_failingCount, RETRYCOUNT);
			usleep(500 * 1000);

		} else // else success
		{
			L_fSerialPortOpen = TRUE;
		}
	}
	return(L_fSerialPortOpen);
}

/*******************************************************************************
 * Function:		equalArrays
 * Parameters(s):	Pointer to char array
 * 					Pointer to char array
 * 					Size of second char array
 * Returns:			TRUE or FALSE
 * Description:		This function checks if two unsigned char array are equal or
 * 					not with respect to the size of the second char array
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *******************************************************************************/
static BOOLEAN equalArrays (const INT8U *P_p1, const INT8U *P_p2, const size_t *P_size2)
{
	INT8U i;
	BOOLEAN L_fEqual = TRUE;

	for(i = 0; i < *P_size2; i++)
	{
		if (P_p1[i] != P_p2[i])
		{
			L_fEqual = FALSE;
			break;
		}
	}

	return(L_fEqual);
}

/*******************************************************************************
 * Function:		ledDriver_convertValueToMsg
 * Parameters(s):	Pointer to value. MAX 65535
 * 					Pointer to the message
 * Returns:
 * Description:		This function covert a INT16U to a three byte c string.
 * 					In case of a Linux 64 bit system the third and fourth byte
 * 					are ignored.
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *******************************************************************************/
static void ledDriver_convertValueToMsg( const INT16U *P_value, INT8U *P_msg)
{
	// copy 2-bytes from INT16 to INT8. Rest of bytes are ignored.
	memcpy( P_msg, P_value, 2);

	// add NULL terminating character
	P_msg += 2;
	*P_msg = '\0';
	P_msg -= 2;
}

/*******************************************************************************
 * Function:		ledDriver_convertMsgToValue
 * Parameters(s):	Pointer to the message
 * 					Pointer to value. MAX 65535
 * Returns:
 * Description:		This function covert a INT16U to a three byte c string.
 * 					In case of a Linux 64 bit system the third and fourth byte
 * 					are ignored.
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *******************************************************************************/
static void ledDriver_convertMsgToValue( const INT8U *P_msg, INT16U *P_value)
{
	// copy 2-bytes from INT16 to INT8. Rest of bytes are ignored.
	memcpy( P_value, P_msg, 2);

	// First two bytes are numbers. rest is 0

	P_value += 2;
	*P_value = '0'; // third byte is 0
	P_value++;
	*P_value = '0'; // fourth byte is 0
	P_value -= 4; // reset ptr to first

}

/*******************************************************************************
 * Function:		initLedDrivers
 * Parameters(s):
 * Returns:
 * Description:		This function initialize the led drivers structures with
 * 					some initial values
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *******************************************************************************/
static void ledDriver_init()
{
	INT8U i = 0;
	size_t L_size = 0;
	L_size = (sizeof(G_stLedDriver) / sizeof(G_stLedDriver[0]));
	for(i = 0; i < L_size; i++)
	{
		G_stLedDriver[i].id = i;
		G_stLedDriver[i].newValue = TRUE;
		G_stLedDriver[i].value = ((i * 1000) + 1);
		pthread_mutex_init(&G_stLedDriver[i].threadLock, NULL); // Initialize mutexen
	}
}

/*******************************************************************************
 * Function:		newValues
 * Parameters(s):
 * Returns:			If new values is present in one of the struct then it returns
 * 					the first struct number where this is. else return -1.
 * Description:		This function checks if there are new values present in
 * 					the struct by checking the flags of each struct
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *******************************************************************************/
static INT8U ledDriver_newValue(const INT8U *P_threadID, INT8U *P_driverNr)
{
	INT8U i = 0;
	INT8U rc = FALSE;
	size_t L_size = 0;
	*P_driverNr = 0; // init value is 0 (no new value)

	L_size = (sizeof(G_stLedDriver) / sizeof(G_stLedDriver[0]));

	// Check every value of a struct if there is a new value. If so, return this number
	for(i = 0; i < L_size; i++)
	{
		if (EBUSY != pthread_mutex_trylock(&G_stLedDriver[i].threadLock)) // check if another thread  blocking this driver. If not then lock
		{
			if (G_stLedDriver[i].newValue == TRUE)
			{
				*P_driverNr = ( i + 1 ); // + 1 for change driver number from 0..n to 1..n so that 0 is no new value
				rc = TRUE;
				break;
			} else // if no new value for driver..
			{
				pthread_mutex_unlock(&G_stLedDriver[i].threadLock); // unlock locked driver
			}
		} else // Driver is locked and used by another thread
		{
			printf("Thread[%d]:Led Driver: Driver [%d] is locked\n", *P_threadID, (i + 1));
		}
	}
	return (rc); // return driver number. 0 = no new value
}

/*******************************************************************************
 * Function:		MQTT_thread
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
