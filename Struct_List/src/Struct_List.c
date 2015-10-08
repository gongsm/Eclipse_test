/*
 ============================================================================
 Name        : Struct_List.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include "struct_list.h"


List CreateList()
{
	List head;
	head = (List)malloc(sizeof(struct Node));
	head->next = NULL;
	head->x = -65536;
	return head;
}
int IsEmpty(List L)
{
	if(L->next == NULL)
	{
		return 1;
	}
	else
		return 0;
}
Position FindPrevious(List L, Position p)
{
	Position next;
	next = L;
	while(next->next != p)
		next = next->next;
	if(next->next == NULL)
		return NULL;
	return next;
}
void InsertList(List L, int x)
{
	List next = L;
	List p = (List)malloc(sizeof(struct Node));
	p->x = x;
	p->next = NULL;
	if(IsEmpty(L))
	{
		L->next = p;
		return;
	}
	while(next->next !=NULL && next->next->x < x )
	{
	  next = next->next;
	}

	p->next = next->next;
	next->next = p;
}

Position Find(List L, int x)
{
	Position p = L->next;
	while(p!=NULL && p->x != x)
	{
			p = p->next;
	}
	return p;
}

void DeleteElement(List L,int x)
{
   Position temp;
   Position next = L;
   while(next->next !=NULL && next->next->x != x)
   {
	   next = next->next;
   }
   if(next->next !=NULL)
   {
	   temp = next->next;
	   next->next = temp->next;
	   free(temp);
   }
}


void printlist(List L)
{
	Position p = L->next;
	int i = 0;
	while(p!=NULL)
	{
		i++;
		printf("%d  ",p->x);
		p = p->next;
	}
	printf("\n");
}
