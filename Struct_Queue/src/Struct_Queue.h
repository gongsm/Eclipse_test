typedef struct Node
{
  int size;
  int rd_pos;
  int wr_pos;
  int *array;
}QueueRecord, *Queue;

Queue CreateQueue(int maxsize);

int IsEmpty(Queue Q);

int IsFull(Queue Q);

void Enqueue(int ele,Queue Q);

int Dequeue(Queue Q);
