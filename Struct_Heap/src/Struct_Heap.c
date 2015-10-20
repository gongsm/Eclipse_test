/*
 ============================================================================
 Name        : Struct_Heap.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include "Struct_Heap.h"
PriorityQueue Initialize(int max)
{
	PriorityQueue H = malloc(sizeof(HeapStruct));
	if(H==NULL)
	{
		printf("out of space!");
		return NULL;
	}
	H->element = malloc((max+1)*sizeof(int));
	if(H->element==NULL)
	{
		printf("out of space");
		return NULL;
	}
	H->capacity = max;
	H->size = 0;
	H->element[0] = -9999;
	return H;
}

int IsFull(PriorityQueue H)
{
	return H->size == H->capacity;
}
int IsEmpty(PriorityQueue H)
{
	return H->size==0;
}
void Insert(int x, PriorityQueue H)
{
	int i;
	if(IsFull(H))
	{
		printf("the queue is full");
		return;
	}
	H->size++;
	for(i=H->size;H->element[i/2]>x;i=i/2)
	{
		H->element[i] = H->element[i/2];
	}

	H->element[i] = x;

}
void Destroy(PriorityQueue H)
{
	if(H !=NULL)
	{
		if(H->element!=NULL)
		   free(H->element);
	    free(H);
	}
}
void MakeEmpty(PriorityQueue H)
{
	if(H!=NULL)
	{
		if(H->element!=NULL)
		{
			H->size = 0;
		}
	}
}


int DeleteMin(PriorityQueue H)
{
	int data,i=1;
	if(IsEmpty(H))
	{
		printf("is empty");
		return H->element[0];
	}
	data = H->element[1];
    while(2*i<H->size && (2*i+1)<H->size)
    {
    	if(H->element[H->size] < H->element[i])
    		break;
    	if(H->element[2*i] > H->element[2*i+1])
    	{
    		H->element[i] = H->element[2*i+1];
    		i = 2*i+1;
    	}
    	else
    	{
    		H->element[i] = H->element[2*i];
    		i = 2*i;
    	}
    }
    H->element[i] = H->element[H->size];
    H->size--;
	return data;

}
void printheap(PriorityQueue H)
{
	int i;
	if(H!=NULL)
	{
		for(i=1;i<=H->size;i++)
			printf("%d  ",H->element[i]);
	}
	printf("\n");
}
