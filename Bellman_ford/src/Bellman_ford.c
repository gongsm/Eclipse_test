/*
 ============================================================================
 Name        : Bellman_ford.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#define MAX 9999
#define N 1000
typedef struct Edge
{
	int u;
	int v;
	int cost;
}Edge;

Edge edge[N];
int dis[N];
int pre[N];

void Initialize_source(int n,int s)
{
	int i = 1;
	for(;i<=n;i++)
	{
		dis[i] = MAX;
		pre[i] = 0;
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

void printpath(int n)
{
	while(n!=pre[n]&&n!=0)
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
	int edgenum = 10;
	int i=0;
	int j=0;
	edge[1].u = 1;
	edge[1].v = 2;
	edge[1].cost = 6;

	edge[2].u = 1;
	edge[2].v = 5;
	edge[2].cost = 7;

	edge[3].u = 2;
	edge[3].v = 3;
	edge[3].cost = 5;

	edge[4].u = 2;
	edge[4].v = 5;
	edge[4].cost = 8;

	edge[5].u = 2;
	edge[5].v = 4;
	edge[5].cost = -4;

	edge[6].u = 3;
	edge[6].v = 2;
	edge[6].cost = -2;

	edge[7].u = 4;
	edge[7].v = 3;
	edge[7].cost = 7;

	edge[8].u = 4;
	edge[8].v = 1;
	edge[8].cost = 2;

	edge[9].u = 5;
	edge[9].v = 4;
	edge[9].cost = 9;

	edge[10].u = 5;
	edge[10].v = 3;
	edge[10].cost = -3;

	Initialize_source(nodenum,original);
    for(i=1;i<nodenum;i++)
    {
    	for(j=1;j<=edgenum;j++)
    	{
    		Relax(edge[j].u,edge[j].v,edge[j].cost);
    	}
    }
    for(i=1;i<=nodenum;i++)
    {
    	printf("1->%d:%d   ",i,dis[i]);
    }
    printf("\n");
    printpath(3);

	return EXIT_SUCCESS;
}


/*
#define INF 99999
int map[5][5]={
	INF,6,INF,INF,7,
    INF,INF,5,-4,8,
	INF,-2,INF,INF,INF,
	2,INF,7,INF,INF,
	INF,INF,-3,9,INF
};
int dist[5];

int Bellman_ford(int n, int s)
{
    int v, u,i;

    for (v=0; v<n; v++)
    {
       // if (map[s][v] == INF)
            dist[v] = INF;
       //    else
       //    dist[v] = map[s][v];
    }

    dist[s] = 0;
  for(i=1;i<n;i++)
    for (v=0; v<n; v++)
        for (u=0; u<n; u++)
            if (map[u][v] < INF)  //u->v has path
                if (dist[v] > dist[u] + map[u][v])
                    dist[v] = dist[u] + map[u][v];

    //遍历所有的边
    for (v=0; v<n; v++)
        for (u=0; u<n; u++)
            if (v != u && map[u][v] != INF)
                if (dist[v] > dist[u] + map[v][u])
                    return 0;

    return 1;
}

void PrintMap(int n)
{
    int i, j;
    //输出矩阵
    for (i=0; i<n; i++)
    {
        for (j=0; j<n; j++)
        {
            if (map[i][j] == INF)
                printf("INF ");
            else
                printf("%d  ", map[i][j]);
        }

        printf("\n");
    }
}

void PrintShortestValue(int n)
{
    int i;

    for (i=0; i<n; i++)
        printf("%d:%d ", i, dist[i]);
    printf("\n");
}


int main(void){

	int n=5;
	 Bellman_ford(n, 1);
	 PrintShortestValue(n);
	return EXIT_SUCCESS;
}
*/
