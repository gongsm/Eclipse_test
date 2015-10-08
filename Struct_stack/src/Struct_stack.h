typedef struct Node
{
  int x;
  struct Node *next;
}*PtrToNode;

typedef PtrToNode Stack;

int IsEmpty(Stack S);
Stack CreateStack(void);
void Push(Stack S, int element);
int Pop(Stack S);
