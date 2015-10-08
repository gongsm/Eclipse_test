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
#include "struct_stack.h"

int main(void) {
	Stack S;
	int i=0;
	int data;
	S = CreateStack();
	for(i=0;i<10;i++)
		Push(S,i);
	for(i=0;i<10;i++)
	{
		data = Pop(S);
		printf("%d  ",data);
	}
}
