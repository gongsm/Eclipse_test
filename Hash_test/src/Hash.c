/*
 ============================================================================
 Name        : hash.c
 Author      :
 Version     :
 Copyright   : Your copyright notice
 Description : define and imcompelite the method of hash
 ============================================================================
 */
#include <stdio.h>
#include <stdlib.h>
#include "hash.h"

HashTable InitTalbe(int tablesize)
{
	HashTable H;
	int i = 0;
	H = malloc(sizeof(HashTbl));
	if(H==NULL)
	{
		printf("out of space");
		return NULL;
	}
	H->tablesize = tablesize;
	H->TheList = malloc(sizeof(List)*tablesize);
	if(H->TheList == NULL)
	{
		printf("out of space");
		return NULL;
	}
	for(i=0;i<tablesize;i++)
	{
		H->TheList[i] = malloc(sizeof(ListNode));
		if(H->TheList[i]==NULL)
		{
			printf("out of space!");
			return NULL;
		}
		else
			H->TheList[i]->next = NULL;
	}

	return H;
}

static void DestroyList(List L)
{
	List temp;
	while(L->next!=NULL)
	{
		temp = L->next;
		L->next = temp->next;
		free(temp);
	}
	if(L!=NULL)
		free(L);
}
void DestroyTable(HashTable H)
{
	int i = 0;
	for(i=0;i<H->tablesize;i++)
	{
		DestroyList(H->TheList[i]);

	}
}

int Hash(int key, int tablesize)
{
	return key%tablesize;
}

Position Find(int ele,HashTable H)
{
    List L;
    Position P=NULL;
    L = H->TheList[Hash(ele,H->tablesize)];
    P = L->next;
    while(P!=NULL&&P->element!=ele)
    {
    	P = P->next;
    }
    return P;
}

void Insert(int x,HashTable H)
{
	Position P;
	int index;
	P = Find(x,H);
	if(P!=NULL)
	{
		printf("the ele has in table");
		return;
	}
	index = Hash(x,H->tablesize);

    P = malloc(sizeof(ListNode));
	if(P == NULL)
	{
		printf("no space to insert!");
		return;
	}
	P->element = x;
	P->next = H->TheList[index]->next;
	H->TheList[index]->next = P;
}

void printHash(HashTable H)
{
	int i = 0;
	Position p;
	for(i = 0;i<H->tablesize;i++)
	{
		p = H->TheList[i];
		while(p->next!=NULL)
		{
			printf("%d  ",p->next->element);
			p = p->next;
		}
		printf("\n");
	}
}
