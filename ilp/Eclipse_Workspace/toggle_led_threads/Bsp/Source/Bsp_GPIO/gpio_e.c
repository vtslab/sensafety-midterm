/*
================================================================================
  (c) 2014 Strukton Embedded Solutions

  Project/Module: GPIO driver for embedded Linux

  Description: Functions for controlling GPIO in- and outputs

  Reference:

  Version Control
  	  $workfile: gpio_e.c
  	  $Revision:
  	  $Date: 08-04-2014
  	  Modtime:

================================================================================
 */

#include "Bsp/Include/Bsp_GPIO/gpio_e.h"

/*******************************************************************************
 * Function:		GPIOExport
 * Parameters(s):	INT8U P_pin
 * 						Contains the header pin on the board
 * Returns:			Returns '-1' on failure or '0' when OK
 * Description:		Function to make a GPIO Export file on an specific pin
 * Reference:		http://elinux.org/RPi_Low-level_peripherals#C_.2B_sysfs
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
INT8U GPIOExport(INT8U P_pin)
{

	char buffer[BUFFER_MAX];
	ssize_t bytes_written; // ssize_t = signed integer type
	int fd; // File descriptor

	fd = open("/sys/class/gpio/export", O_WRONLY); // open file for write access
	if (-1 == fd) {
		fprintf(stderr, "Failed to open export for writing\n");
		return(-1);
	}

	bytes_written = snprintf(buffer, BUFFER_MAX, "%d", P_pin);
	write(fd, buffer, bytes_written);
	close(fd);
	return(0);
}

/*******************************************************************************
 * Function:		GPIOUnexport
 * Parameters(s):	INT8U P_pin
 * 						Contains the header pin on the board
 * Returns:			Returns '-1' on failure or '0' when OK
 * Description:		Function to unexport GPIO Export file on an specific pin
 * Reference:		http://elinux.org/RPi_Low-level_peripherals#C_.2B_sysfs
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
INT8U GPIOUnexport(INT8U P_pin)
{
	char buffer[BUFFER_MAX];
	ssize_t bytes_written;
	int fd;

	fd = open("/sys/class/gpio/unexport", O_WRONLY);
	if (-1 == fd) {
		fprintf(stderr, "Failed to open unexport for writing!\n");
		return(-1);
	}

	bytes_written = snprintf(buffer, BUFFER_MAX, "%d", P_pin);
	write(fd, buffer, bytes_written);
	close(fd);
	return(0);
}

/*******************************************************************************
 * Function:		GPIODirection
 * Parameters(s):	INT8U P_pin
 * 						Contains the header pin on the board
 * 					INT8U dir
 * 						Specify the direction (IN or OUT) of the pin
 * Returns:			Returns '-1' on failure or '0' when OK
 * Description:		Function to set the direction of an pin
 * Reference:		http://elinux.org/RPi_Low-level_peripherals#C_.2B_sysfs
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
INT8U GPIODirection(INT8U P_pin, INT8U P_dir)
{
	static const char s_directions_str[]  = "in\0out";

	char path[DIRECTION_MAX];
	int fd;

	snprintf(path, DIRECTION_MAX, "/sys/class/gpio/gpio%d/direction", P_pin);
	fd = open(path, O_WRONLY);
	if (-1 == fd) {
		fprintf(stderr, "Failed to open gpio direction for writing!\n");
		return(-1);
	}

	if (-1 == write(fd, &s_directions_str[IN == P_dir ? 0 : 3], IN == P_dir ? 2 : 3)) {
		fprintf(stderr, "Failed to set direction!\n");
		return(-1);
	}

	close(fd);
	return(0);
}

/*******************************************************************************
 * Function:		GPIORead
 * Parameters(s):	INT8U P_pin
 * 						Contains the header pin on the board
 * Returns:			Returns '-1' on failure or '0' when OK
 * Description:		Function to read the value of an specific pin
 * Reference:		http://elinux.org/RPi_Low-level_peripherals#C_.2B_sysfs
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
INT8U GPIORead(INT8U P_pin)
{

	char path[VALUE_MAX];
	char value_str[3];
	int fd;

	snprintf(path, VALUE_MAX, "/sys/class/gpio/gpio%d/value", P_pin);
	fd = open(path, O_RDONLY);
	if (-1 == fd) {
		fprintf(stderr, "Failed to open gpio value for reading!\n");
		return(-1);
	}

	if (-1 == read(fd, value_str, 3)) {
		fprintf(stderr, "Failed to read value!\n");
		return(-1);
	}

	close(fd);

	return(atoi(value_str));
}

/*******************************************************************************
 * Function:		GPIOWrite
 * Parameters(s):	INT8U P_pin
 * 						Contains the header pin on the board
 * 					INT8U value
 * 						Specify the wanted value of the pin
 * Returns:			Returns '-1' on failure or '0' when OK
 * Description:		Function to write a value to an header pin
 * Reference:		http://elinux.org/RPi_Low-level_peripherals#C_.2B_sysfs
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
INT8U GPIOWrite(INT8U P_pin, INT8U P_value)
{
	static const char s_values_str[] = "01";

	char path[VALUE_MAX];
	int fd;

	snprintf(path, VALUE_MAX, "/sys/class/gpio/gpio%d/value", P_pin);
	fd = open(path, O_WRONLY);
	if (-1 == fd) {
		fprintf(stderr, "Failed to open gpio value for writing!\n");
		return(-1);
	}

	if (1 != write(fd, &s_values_str[LOW == P_value ? 0 : 1], 1)) {
		fprintf(stderr, "Failed to write %d to %d!\n", P_pin, P_value);
		return(-1);
	}

	close(fd);
	return(0);
}

/*******************************************************************************
 * Function:		toggleOutput
 * Parameters(s):	INT8U P_pin
 * 						Contains the header pin on the board
 * Returns:			Returns '-1' on failure or '0' when OK
 * Description:		Function to toggle an output
 * Reference:		http://elinux.org/RPi_Low-level_peripherals#C_.2B_sysfs
 * Global/static variables
 * 		modified:	--
 * 		used:		--
 * Error handling:	--
 *
 *******************************************************************************/
INT8U toggleOutput(INT8U P_pin)
{
	/*
	 * Read GPIO value
	 */
	if (1 == GPIORead(P_pin))
	{
		/*
		 * Write GPIO value
		 */
		if (-1 == GPIOWrite(P_pin, 0))
		{
			return(3);
		}
	}
	else
	{
		/*
		 * Write GPIO value
		 */
		if (-1 == GPIOWrite(P_pin, 1))
		{
			return(3);
		}
	}
	return(0);
}
