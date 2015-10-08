

typedef struct Node
{
  int x;
  struct Node *next;
}*PtrToNode;

typedef PtrToNode List;
typedef PtrToNode Position;

List CreateList();
void InsertList(List L, int x);
int IsEmpty(List L);
Position Find(List L, int x);
Position FindPrevious(List L, Position p);
void DeleteElement(List L,int x);
void printlist(List L);


