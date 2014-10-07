/*
 ============================================================================
 Name        : charren.c
 Author      : Jeffrey
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
	puts("!!!Hello World!!!"); /* prints !!!Hello World!!! */

	char message[4];
	char driver = 0;
	char breakChar = '/';
	char value = 255;


	strcpy( &message, &driver);
	strcat( &message, &breakChar);
	strcat( &message, &value);

	return EXIT_SUCCESS;
}
