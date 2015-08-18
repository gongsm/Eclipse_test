/*
 ============================================================================
 Name        : malloc_test.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>


int main(void) {
	char * p1;
		char * p2;
		char * p3;
		char * p4;
		int i=1;
		int test;
		p4 = (char *)malloc(500*sizeof(char));
		printf("%d\n",sizeof(char *));
		for(;i<20;i++)
		{
			p1=NULL;
			p2=NULL;
			p3=NULL;

			p1=(char *)malloc(i*sizeof(char));
	        p2=(char *)malloc(1*sizeof(char));
			test = p2-p1;
			printf("i=%d     %d\n",i,test);
			if(p4!=NULL)
			{
				free(p4);
				p4 = NULL;
			}

		}
	return EXIT_SUCCESS;
}

