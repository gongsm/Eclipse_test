#include <stdio.h>
#include <stdlib.h>
#include "struct_stack.h"


Stack CreateStack(void)
{
	Stack S;
	S= (Stack)malloc(sizeof(struct Node));
	S->next = NULL;
	return S;
}

int IsEmpty(Stack S)
{
	return S->next == NULL;
}

void Push(Stack S, int x)
{
	Stack temp;
	temp = (Stack)malloc(sizeof(struct Node));
	if(temp == NULL)
	{
		printf("Out of Space!");

	}
	else
	{
		temp->x = x;
		temp->next = S->next;
		S->next = temp;
	}
}

int Pop(Stack S)
{
	int data;
	Stack temp;
	if(IsEmpty(S))
	{
		printf("empty stack!");
		return 0;
	}
	else
	{
		temp = S->next;
		data = S->next->x;
		S->next = temp->next;
		free(temp);
		return data;
	}

}
