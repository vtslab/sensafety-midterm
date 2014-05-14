/*
================================================================================
  (c) 2014 Strukton Embedded Solutions

  Project/Module: Serial driver for embedded Linux

  Description: Functions for controlling serial in- and outputs

  Reference:

  Version Control
  	  $workfile: serial.c
  	  $Revision:
  	  $Date: 08-04-2014
  	  Modtime:

================================================================================
 */

#include "App/Source/LampDriver/LampDriver.h"
#include "App/Source/MqttBroker/MqttBroker.h"


/*******************************************************************************
 * Function:		initializeSerial
 * Parameters(s):
 * Returns:			Returns '-1' on failure or '0' when OK
 * Description:		Function to initialize serial communication
 * Reference:		http://www.raspberry-projects.com/pi/programming-in-c/uart-serial-port/using-the-uart
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
INT8U initLampDriverComm()
{
	/*
          Open modem device for reading and writing
	 */

	uart0_fd = open(SERIALDEVICE, O_RDWR | O_NOCTTY | O_NDELAY);
	if (uart0_fd == -1)
	{
		return (uart0_fd);
	}

	/* Struct for port settings */
	struct termios options;

	/* input mode flags
		IGNPAR 	: 	ignore bytes with parity errors
		ICRNL 	: 	map CR to NL (otherwise a CR input on the other computer
					will not terminate input)
					otherwise make device raw (no other input processing)
	*/
	options.c_iflag = IGNPAR | ICRNL;

	/* output mode flags
	 		RAW output
	 */
	options.c_oflag = 0;

	/* control mode flags
	 	BAUDRATE: 	Set bps rate. You could also use cfsetispeed and cfsetospeed.
		CS8 	: 	8n1 (8bit,no parity,1 stopbit)
		CLOCAL 	: 	local connection, no modem contol
		CREAD 	: 	enable receiving characters
	 */
	options.c_cflag = SERIALBAUDRATE | CS8 | CLOCAL | CREAD;

	/* local mode flags
	    ICANON : 	enable canonical input
					disable all echo functionality, and don't send signals to calling program
	 */
	options.c_lflag = ICANON | ECHO;

	/* Clean input stream of UART0 */
	tcflush(uart0_fd, TCIFLUSH);
	/* Set port settings */
	tcsetattr(uart0_fd, TCSANOW, &options);

	return(SUCCESS);
}

void CloseUart()
{
	close(uart0_fd);
}

/*******************************************************************************
 * Function:		sendMsgtoLampDriver
 * Parameters(s):
 * Returns:			Returns '-1' on failure or '0' when OK
 * Description:		Thread function to Toggle an led
 * Reference:
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
INT8U sendMsgtoLampDriver(char *P_cString)
{
	if (uart0_fd != -1)
	{
		int count = write(uart0_fd, &P_cString[0], strlen(P_cString));		//File descriptor, bytes to write, number of bytes to write
		if (count < 0) // if nothing is written
		{
			return (count);
		}
	}
	return (SUCCESS);
}

void clearScreen()
{
	sendStringOverUart("\33[2J\33[H");
}

void blinkScreen()
{
	sendStringOverUart("\33[?5h");
	usleep (50 * 1000);
	sendStringOverUart("\33[?5l");
}

void clearLine()
{
	sendStringOverUart("\33[2K");
}

void cursorToLine (INT8U P_line)
{
	char buffer[20];
	sprintf(buffer, "\33[%d;0f", P_line);
	sendStringOverUart(buffer);
}

void cursorToColumn (INT8U P_column)
{
	char buffer[20];
	//First move to the first column.
	sendStringOverUart("\r");
	if (P_column > 0) {
		sprintf(buffer, "\33[%dC", P_column);
		sendStringOverUart(buffer);
	}
}

void terminalReset()
{
	blinkScreen();
	clearScreen();
	cursorToColumn(0);
	cursorToLine(0);
}

void readLine(char * buffer)
{
		if (uart0_fd != -1)
		{
			read(uart0_fd, (void*)buffer, 255);		// Filestream, buffer to store in, number of bytes to read (max)
		}
}
