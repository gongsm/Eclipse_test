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
#include "hash.h"
int main(void) {

	int i;
	HashTable H = InitTalbe(5);
    for(i=0;i<5;i++)
    	Insert(i,H);
    printHash(H);
    Insert(20,H);
    printHash(H);
	return EXIT_SUCCESS;
}
