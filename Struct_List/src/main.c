#include <stdio.h>
#include <stdlib.h>
#include "struct_list.h"

int main(void)
{
	int i = 10;
	List L = CreateList();
	for(;i>0;i--)
	{
		InsertList( L, i);
	}
	printlist(L);
	DeleteElement(L,8);
	printlist(L);
	DeleteElement(L,23);
		printlist(L);
}

