/*数组实现二叉堆*/
typedef struct HeapStruct
{
	int capacity;
	int size;
	int *element;
}HeapStruct,*PriorityQueue;


PriorityQueue Initialize(int maxelement);
void Destroy(PriorityQueue H);
void MakeEmpty(PriorityQueue H);
void Insert(int x,PriorityQueue H);
int DeleteMin(PriorityQueue H);
int IsEmpty(PriorityQueue H);
int IsFull(PriorityQueue H);
void printheap(PriorityQueue H);
