/*
 ============================================================================
 Name        : main.c
 Author      :
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include "Struct_Queue.h"
int main(void) {
/*	int *temp = (int*)malloc(4*sizeof(int));
	int i =1;
	printf("%d  %d",temp,temp+i);*/

	int i=0;
	int data;
	Queue testqueue = CreateQueue(5);
	for(i=0;i<100;i++)
	{
		Enqueue(i,testqueue);
	}
	for(i=0;i<50;i++)
	{
		data = Dequeue(testqueue);
		printf("%d  ",data);
	}
	for(i=100;i<200;i++)
    {
		Enqueue(i,testqueue);
	}
	for(i=0;i<150;i++)
		{
			data = Dequeue(testqueue);
			printf("%d  ",data);
		}
	puts("!!!Hello World!!!"); /* prints !!!Hello World!!! */
	return EXIT_SUCCESS;
}
