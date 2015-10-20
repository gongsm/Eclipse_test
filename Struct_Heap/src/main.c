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
#include "Struct_Heap.h"
int main(void) {
	int i;
	int data;
	PriorityQueue H = Initialize(20);
	for(i=0;i<15;i=i+2)
	{
		Insert(i,H);
	}
	Insert(3,H);
	Insert(7,H);
	printheap(H);
	data = DeleteMin(H);
	printheap(H);
	puts("!!!Hello World!!!"); /* prints !!!Hello World!!! */
	return EXIT_SUCCESS;
}
