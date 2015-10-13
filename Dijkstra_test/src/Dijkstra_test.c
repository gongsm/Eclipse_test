/*
 ============================================================================
 Name        : Dijkstra_test.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#define MAXNODE 100
#define MAX 9999
int dis[MAXNODE];
int pre[MAXNODE];
int isextract[MAXNODE];
typedef struct NodeEdge
{
	int nodenum;
	int weight;
}NodeEdge;
typedef struct  GraphNodeEdge
{
	int node;
	int edgenum;
	NodeEdge edge[MAXNODE];
}GraphNodeEdge;

GraphNodeEdge graph[5] =
{
	[0].node = 0,
	[0].edgenum = 2,
	[0].edge[0] = {1,10},
	[0].edge[1] = {4,5},
	[1].node = 1,
	[1].edgenum = 2,
	[1].edge[0] = {2,1},
	[1].edge[1] = {4,2},

	[2].node = 2,
	[2].edgenum = 1,
	[2].edge[0] = {3,4},

	[3].node = 3,
	[3].edgenum = 2,
	[3].edge[0] = {2,6},
	[3].edge[1] = {0,7},

	[4].node = 4,
	[4].edgenum = 3,
	[4].edge[0] = {1,3},
	[4].edge[1] = {2,9},
	[4].edge[2] = {3,2}
};
void Initialize_source(int n,int s)
{
	int i = 0;
	for(;i<n;i++)
	{
		dis[i] = MAX;
		pre[i] = -1;
		isextract[i] = 0;
	}
	dis[s] = 0;
	pre[s] = s;

}
void Relax(u,v,cost)
{
	if(dis[v]>dis[u]+cost)
	{
		dis[v] = dis[u]+cost;
		pre[v] = u;
	}
}
int Extract_min(int nodenum)
{
	int i;
	int chose =0;
	int min = 999;
	for(i=0;i<nodenum;i++)
	{
		if(isextract[i]==0)
		{
			if(dis[i]<min)
			{
				min = dis[i];
				chose = i;
			}

		}
	}
	isextract[chose] = 1;
	return chose;
}
void printpath(int n)
{
	while(n!=pre[n]&&n!=-1)
	{
		printf("%d<--",n);
		n=pre[n];
	}
	if(n==pre[n])
	{
		printf("%d",n);
	}
}

int main(void) {
	int nodenum = 5;
	int original = 2;
	int i=0,j=0;
	int u;
	Initialize_source(nodenum,original);
    for(i=0;i<nodenum;i++)
    {
    	u = Extract_min(nodenum);
    	for(j=0;j<graph[u].edgenum;j++)
    	{
    		Relax(u,graph[u].edge[j].nodenum,graph[u].edge[j].weight);
    	}
    }
    for(i=0;i<nodenum;i++)
    	printf("%d   ",dis[i]);
    printpath(0);
	puts("!!!Hello World!!!"); /* prints !!!Hello World!!! */
	return EXIT_SUCCESS;
}
