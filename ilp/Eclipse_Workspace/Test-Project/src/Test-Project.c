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

int main(void) {

	char message[4];
	char driver = 0;
	char breakChar = '/';
	char value = 255;


	strcpy( message, driver);
	strcat( message, breakChar);
	strcat( message, value);

	puts("!!!Hello World!!!"); /* prints !!!Hello World!!! */
	return EXIT_SUCCESS;
}

