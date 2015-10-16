/*
 ============================================================================
 Name        : hash.h
 Author      :
 Version     :
 Copyright   : Your copyright notice
 Description : define the hash struct  分离链接散列表
 ============================================================================
 */

struct ListNode;
typedef struct ListNode *Position;
typedef Position List;
struct HashTbl;
typedef struct HashTbl  *HashTable;


typedef struct ListNode
{
	int element;
	Position next;
}ListNode;

typedef struct HashTbl
{
	int tablesize;
	List *TheList;
}HashTbl;

HashTable InitTalbe(int tablesize);
void DestroyTable(HashTable H);
Position Find(int ele,HashTable H);
void Insert(int x,HashTable H);
int Hash(int key, int tablesize);
void printHash(HashTable H);
