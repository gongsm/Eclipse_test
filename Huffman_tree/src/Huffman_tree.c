/*
 ============================================================================
 Name        : Huffman_tree.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>

#define  MAXBIT  100
#define  MAXVALUE 10000
#define  MAXLEAF  30
#define  MAXNODE MAXLEAF*2-1

typedef struct
{
	int bit[MAXBIT];
	int start;
} HCodeType;

typedef struct
{
	int weight;
	int parent;
	int lchild;
	int rchild;
	int value;
} HNodeType;

void HuffmanTree(HNodeType huffnode[MAXNODE], int n)
{
	int i,j,m1,m2,x1,x2;
	for(i=0;i<2*n-1;i++)
	{
		huffnode[i].weight = i;
		huffnode[i].parent = -1;
		huffnode[i].lchild = -1;
		huffnode[i].rchild = -1;
		huffnode[i].value = i;

	}
	for(i=0;i<n-1;i++)
	{
		m1=m2=MAXVALUE;
		x1=x2=0;
		for(j=0;j<n+i;j++)
		{
			if(huffnode[j].weight < m1 && huffnode[j].parent == -1 )
			{
				m2 = m1;
				m1 = huffnode[j].weight;
				x2 = x1;
				x1 = j;
			}
			else if(huffnode[j].weight < m2 && huffnode[j].parent == -1)
			{
				m2 = huffnode[j].weight;
				x2 = j;
			}
		}

		huffnode[x1].parent = n+i;
		huffnode[x2].parent = n+i;
		huffnode[n+i].weight = huffnode[x1].weight + huffnode[x2].weight;
		huffnode[n+i].lchild = x1;
		huffnode[n+i].rchild = x2;
	}
}


void decodeing()
{

}
int main(void) {

	HNodeType huffnode[MAXNODE];
	HCodeType huffcode[MAXLEAF], cd;
	int n = 10;
	int c,p,j,i;
	HuffmanTree(huffnode,n);

	for( i=0;i<n;i++)
	{
		cd.start = n-1;
		c = i;
		p = huffnode[c].parent;
		while(p!=-1)
		{
			if(huffnode[p].lchild == c)
				cd.bit[cd.start] = 0;
			else
				cd.bit[cd.start] = 1;
			cd.start--;
			c = p;
			p = huffnode[c].parent;
		}
		for(j=cd.start+1;j<n;j++)
		{
			huffcode[i].bit[j] = cd.bit[j];
		}
		huffcode[i].start = cd.start;
	}
	for (i=0; i<n; i++)
	    {
	        printf ("%d 's Huffman code is: ", i);
	        for (j=huffcode[i].start+1; j < n; j++)
	        {
	            printf ("%d", huffcode[i].bit[j]);
	        }
	        printf ("\n");
	    }
	puts("!!!Hello World!!!"); /* prints !!!Hello World!!! */
	return EXIT_SUCCESS;
}
