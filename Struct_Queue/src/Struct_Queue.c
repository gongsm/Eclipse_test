#include <stdio.h>
#include <stdlib.h>
#include "Struct_Queue.h"
#define ADDSIZE  100
Queue CreateQueue(int maxsize)
{
	Queue Q = (Queue)malloc(sizeof(struct Node));
	Q->rd_pos = 0;
	Q->wr_pos = 0;
	Q->size = maxsize;
	Q->array = (int *)malloc(maxsize*sizeof(int));
	return Q;
}
int IsEmpty(Queue Q)
{
	return Q->rd_pos == Q->wr_pos;
}

int IsFull(Queue Q)
{
	if((Q->wr_pos+1)%(Q->size) == Q->rd_pos)
	{
		return 1;
	}
	else return 0;
}

void Enqueue(int ele,Queue Q)
{
	if(IsFull(Q))
	{
		printf("the queue is full,we will allocate more memory\n");
		int *temp = Q->array;
		int *addtemp = (int *)malloc((Q->size+ADDSIZE)*sizeof(int));
		if(addtemp == NULL)
		{
			printf("malloc error!\n");
			return;
		}
		if(Q->rd_pos > Q->wr_pos)
		{
			memcpy(addtemp+Q->size-Q->rd_pos,Q->array,(Q->wr_pos+1)*sizeof(int));
			memcpy(addtemp,Q->array+Q->rd_pos,(Q->size-Q->rd_pos)*sizeof(int));
			free(temp);
			Q->array = addtemp;
			Q->rd_pos = 0;
			Q->wr_pos = Q->size -1;
			Q->size = Q->size + ADDSIZE;
		}
		else
		{
			memcpy(addtemp,Q->array,Q->size*sizeof(int));
			free(temp);
			Q->array = addtemp;
			Q->size = Q->size + ADDSIZE;
		}

	}

	Q->array[Q->wr_pos] = ele;
	Q->wr_pos = (Q->wr_pos+1)%(Q->size);
}

int Dequeue(Queue Q)
{
	int data;
	if(IsEmpty(Q))
	{
		printf("the queue is empty!");
		return 0;
	}
	else
	{
		data = Q->array[Q->rd_pos];
		Q->rd_pos = (Q->rd_pos+1)%(Q->size);
		return data;
	}
}
