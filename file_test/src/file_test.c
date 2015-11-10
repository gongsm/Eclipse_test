/*
 ============================================================================
 Name        : file_test.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include "profiler.h"
void swap(int* a, int* b)
{
	START_PROFILING_FUNC
	int c = *a;
	*a = *b;
	*b = c;
	END_PROFILING_FUNC
	return ;
}
int main(void) {
	int i,j;
	int a,b;
	a = 4;
	b = 5;
	INIT_PROFILING("test",2)

	while(1)
	{
		START_PROFILING_FUNC
		for(i = 0;i<1000;i++)
			for(j=0;j<1000;j++)
				swap(&a,&b);
		END_PROFILING_FUNC
	}
	return EXIT_SUCCESS;
}
