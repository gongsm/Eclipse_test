/*
 ============================================================================
 Name        : All_shortest_path.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description :计算每队顶点间的最短路径，动态规划实现
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#define INF 99999
/*O(n^4)  */
void Slow_shortest_paths(int n,int w[][5],int v[][5])
{
	int i,j,k;
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{

			for(k=0;k<n;k++)
			{
				if(v[i][k]+w[k][j]<v[i][j])
				{
					v[i][j] = v[i][k]+w[k][j];
				}
			}
		}

	}


}
/*O(n^3)  */
void Floyd_warshall(int n, int D[][5])
{
	int i,j,k;
	for(k = 0;k<n;k++)
		for(i=0;i<n;i++)
			for(j=0;j<n;j++)
			{
				if(D[i][j] > D[i][k] + D[k][j])
					D[i][j] =  D[i][k] + D[k][j];
			}
}

void printmap(int n, int map[][5])
{
	int i,j;
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			printf("%d  ",map[i][j]);
		}
		printf("\n");
	}
}

int map[5][5] = {
		0,   3,   8,   INF,   -4,
		INF, 0, INF,   1,      7,
		INF, 4,   0,   INF,   INF,
		2,   INF, -5,  0,     INF,
		INF, INF,INF,  6,      0
};
int main(void) {

	int i,j,m;
	int n = 5;
	int L[5][5];
	int D[5][5];
	for(i=0;i<n;i++)
		for(j=0;j<n;j++)
		{
			L[i][j] = map[i][j];
			D[i][j] = map[i][j];
		}

	for(m=0;m<n;m++)
		Slow_shortest_paths(n,map,L);
	Floyd_warshall(n,D);
	printmap(5,L);
	puts("!!!Hello World!!!"); /* prints !!!Hello World!!! */
	printmap(5,D);
	return EXIT_SUCCESS;
}
