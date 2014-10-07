/*
================================================================================
  (c) 2014 Strukton Embedded Solutions

  Project/Module: toggle_led

  Description: Toggle of an led on the Raspberry PI

  Reference:

  Version Control
  	  $workfile: main.c
  	  $Revision:
  	  $Date: 08-04-2014
  	  Modtime:

================================================================================
 */

#include "App/Include/main.h"

int main(int argc, char *argv[])
{
	initializeLeds();

	pthread_t thread_ledGreen, thread_ledYellow, thread_ledRed;

	fprintf(stderr, "In main creating threads");

	pthread_create(&thread_ledGreen, NULL, (void*) ledTicker, (void *) &G_stGreenLed);
	pthread_create(&thread_ledYellow, NULL, (void*) ledTicker, (void *) &G_stYellowLed);
	pthread_create(&thread_ledRed, NULL, (void*) ledTicker, (void *) &G_stRedLed);

	fprintf(stderr, "Threads created");

	while(1)
	{
	}

	clearGpio();
	return(0);
}

/*******************************************************************************
 * Function:		initializeGpio
 * Parameters(s):
 * Returns:			Returns '-1' on failure or '0' when OK
 * Description:		Function to initialize the GPIO`s
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
static INT8U initializeLeds ()
{
	/*
	 * Enable GPIO pins
	 */
	if (-1 >= GPIOExport(LEDGREEN))

	{
		fprintf(stderr, "Failed to export [%d]\n", LEDGREEN);
		return(-1);
	}
	if (-1 >= GPIOExport(LEDYELLOW))

	{
		fprintf(stderr, "Failed to export [%d]\n", LEDYELLOW);
		return(-1);
	}
	if (-1 >= GPIOExport(LEDRED))
	{
		fprintf(stderr, "Failed to export [%d]\n", LEDRED);
		return(-1);
	}
	if (-1 >= GPIOExport(BUTTON))
	{
		return(-1);
	}
	usleep(250 * 1000); // wait 250ms after exporting files
	/*
	 * Set GPIO directions
	 */
	if (-1 >= GPIODirection(LEDGREEN, OUT))
	{
		fprintf(stderr, "Failed to set direction [%d] to pin [%d]\n",OUT, LEDGREEN);
		return(-1);
	}
	if (-1 >= GPIODirection(LEDYELLOW, OUT))
	{
		fprintf(stderr, "Failed to set direction [%d] to pin [%d]\n",OUT, LEDYELLOW);
		return(-1);
	}
	if (-1 >= GPIODirection(LEDRED, OUT))
	{
		fprintf(stderr, "Failed to set direction [%d] to pin [%d]\n",OUT, LEDRED);
		return(-1);
	}

	if (-1 >= GPIODirection(BUTTON, IN))
	{
		fprintf(stderr, "Failed to set direction [%d] to pin [%d]\n",OUT, BUTTON);
		return(-1);
	}


	G_stGreenLed.ledPin = ledPinGreen;
	G_stGreenLed.intervalTime = 1000;
	strncpy(G_stGreenLed.ledColor, "Green", sizeof(G_stGreenLed.ledColor));

	G_stYellowLed.ledPin = ledPinYellow;
	G_stYellowLed.intervalTime = 1000;
	strncpy(G_stYellowLed.ledColor, "Yellow", sizeof(G_stYellowLed.ledColor));

	G_stRedLed.ledPin = ledPinRed;
	G_stRedLed.intervalTime = 1000;
	strncpy(G_stRedLed.ledColor, "Red", sizeof(G_stRedLed.ledColor));

	return(1);
}

/*******************************************************************************
 * Function:		clearGpio
 * Parameters(s):
 * Returns:			Returns '-1' on failure or '0' when OK
 * Description:		Function to clear the GPIO`s
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
static INT8U clearGpio ()
{
	if (GPIORead(LEDGREEN))
	{
		toggleOutput(LEDGREEN);
	}
	if (GPIORead(LEDYELLOW))
	{
		toggleOutput(LEDYELLOW);
	}
	if (GPIORead(LEDRED))
	{
		toggleOutput(LEDRED);
	}
	/*
	 * Disable GPIO pins
	 */
	if (-1 == GPIOUnexport(LEDGREEN))
	{
		return(-1);
	}
	if (-1 == GPIOUnexport(LEDYELLOW))
	{
		return(-1);
	}
	if (-1 == GPIOUnexport(LEDRED))
	{
		return(-1);
	}
	if (-1 == GPIOUnexport(BUTTON))
	{
		return(-1);
	}

	return(0);
}


static void ledTicker(void *P_threadArg)
{

	G_stLed *L_pStArg;
	L_pStArg = (G_stLed *) P_threadArg;
	INT8U L_pin = L_pStArg->ledPin;
	INT16U L_time = L_pStArg->intervalTime;
	char L_color[100];
	strncpy(L_color,L_pStArg->ledColor, sizeof(L_color));
	/*
	 * Toggle led
	 */
	while(1)
	{
		toggleOutput(L_pin);
		fprintf(stderr, "Thread ledTicker: pin %d with color %s and interval time %d toggled\n", L_pin, L_color, L_time);
		usleep(L_time * 1000);

	}
}



