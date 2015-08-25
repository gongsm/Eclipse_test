/*
 ============================================================================
 Name        : RB_tree.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#define RED 1
#define BLACK 0

typedef struct rbnode
{
	int key;
	int color;
	struct rbnode *lchild,*rchild,*parent;
}rb_node_t,*RBT;


rb_node_t nil;

rb_node_t* rb_newnode(int key)
{
	rb_node_t* node = (rb_node_t*)malloc(sizeof(rb_node_t));
	node->key = key;

	return node;
}
rb_node_t* rb_rotate_left(rb_node_t* root,rb_node_t* nodex)
{
	rb_node_t* nodey = nodex->rchild;
	if(nodey != &nil)
	{
		nodex->rchild = nodey->lchild;
		nodey->lchild->parent = nodex;
		nodey->parent = nodex->parent;
		if(nodex->parent == &nil)
		{
			root = nodey;
		}
		else
		{
			if (nodex == nodex->parent->lchild) nodex->parent->lchild = nodey;
			else                                nodex->parent->rchild = nodey;
		}
		nodey->lchild = nodex;
		nodex->parent = nodey;
		return root;
	}
	else
		return root;
}

rb_node_t* rb_rotate_right(rb_node_t* root,rb_node_t* nodex)
{
	rb_node_t* nodey = nodex->lchild;
	if(nodey != &nil)
	{
		nodex->lchild = nodey->rchild;
		nodey->rchild->parent = nodex;
		nodey->parent = nodex->parent;
		if(nodex->parent == &nil)
		{
			root = nodey;
		}
		else
		{
			if(nodex == nodex->parent->lchild) nodex->parent->lchild = nodey;
			else                               nodex->parent->rchild = nodey;
		}
		nodey->rchild = nodex;
		nodex->parent = nodey;
		return root;
	}

	else
	 return root;
}

rb_node_t* rb_insert_fixup(rb_node_t* root, rb_node_t* nodez)
{
	rb_node_t* nodey;
	while(nodez->parent->color == RED)
	{
		if(nodez->parent == nodez->parent->parent->lchild)
		{
			nodey = nodez->parent->parent->rchild;
			if(nodey->color == RED)
			{
				nodez->parent->color = BLACK;
				nodey->color = BLACK;
                nodey->parent->color = RED;
                nodez = nodez->parent->parent;
			}
			else
			{
				if(nodez == nodez->parent->rchild)
				{
					nodez = nodez->parent;
					root = rb_rotate_left(root,nodez);
				}
				nodez->parent->color = BLACK;
				nodez->parent->parent->color = RED;
				root = rb_rotate_right(root,nodez->parent->parent);
			}
		}
		else
		{
			nodey = nodez->parent->parent->lchild;
			if(nodey->color == RED)
			{
				nodez->parent->color = BLACK;
				nodey->color = BLACK;
			    nodey->parent->color = RED;
			    nodez = nodez->parent->parent;
			}
			else
			{
				if(nodez == nodez->parent->lchild)
				{
					nodez = nodez->parent;
					root = rb_rotate_right(root,nodez);
				}
				nodez->parent->color = BLACK;
				nodez->parent->parent->color = RED;
				root = rb_rotate_left(root,nodez->parent->parent);
			}
		}

	}

	root->color = BLACK;
	return root;
}

rb_node_t* rb_insert(rb_node_t* root, int key)
{
	rb_node_t* nodey = &nil;
	rb_node_t* nodex = root;
	rb_node_t* nodez = rb_newnode(key);
    while(nodex != &nil)
    {
    	nodey = nodex;
    	if(nodez->key < nodex->key) nodex = nodex->lchild;
    	else                        nodex = nodex->rchild;
    }
    nodez->parent = nodey;
    if(nodey == &nil)  root = nodez;
    else
    {
    	if(nodez->key < nodey->key)      nodey->lchild = nodez;
        else                             nodey->rchild = nodez;
    }
    nodez->lchild = &nil;
    nodez->rchild = &nil;
    nodez->color = RED;
    root = rb_insert_fixup(root,nodez);
	return root;
}

rb_node_t* rb_minimum(rb_node_t* nodex)
{
	while(nodex->lchild != &nil)
		nodex = nodex->lchild;
	return nodex;
}

rb_node_t* rb_maximum(rb_node_t* nodex)
{
	while(nodex->rchild != &nil)
		nodex = nodex->rchild;
	return nodex;
}

rb_node_t* rb_successor(rb_node_t* nodex)
{
	rb_node_t* nodey;

	if(nodex->rchild != &nil)
	{
		return rb_minimum(nodex->rchild);
	}

	nodey = nodex->parent;
	while (nodey != &nil && nodex == nodey->rchild)
	{
		nodex = nodey;
		nodey = nodey->parent;
	}
	return nodey;
}

rb_node_t* rb_predecessor(rb_node_t* nodex)
{
	rb_node_t* nodey;

	if(nodex->lchild != &nil)
	{
		return rb_maximum(nodex->rchild);
	}

	nodey = nodex->parent;
	while (nodey != &nil && nodex == nodey->lchild)
	{
		nodex = nodey;
		nodey = nodey->parent;
	}
	return nodey;
}

rb_node_t* rb_delete_fixup(rb_node_t* root,rb_node_t* nodex)
{
	return root;
}

rb_node_t* rb_delete(rb_node_t* root,rb_node_t* nodez)
{
	rb_node_t* nodey;
	rb_node_t* nodex;
    if(nodez->lchild == &nil || nodez->rchild == &nil)
    {
    	nodey = nodez;
    }
    else
    	nodey = rb_successor(nodez);
    if(nodez->lchild != &nil)
    	nodex = nodey->lchild;
    else
    	nodex = nodey->rchild;

    nodex->parent = nodey->parent;
    if(nodey->parent == &nil)
    	root = nodex;
    else
    {
      if(nodey == nodey->parent->lchild)
    	  nodey->parent->lchild = nodex;
      else
    	  nodey->parent->rchild = nodex;
    }
    if(nodey != nodez)
    {
    	nodez->key = nodey->key;
    }
    if(nodey->color == BLACK)
    {
    	root = rb_delete_fixup(root,nodex);
    }
    free(nodey);
	return root;
}
void preordertraverse(rb_node_t* root)
{
	if(root != &nil)
		{
			printf("%d  ",root->key);
			preordertraverse(root->lchild);
			preordertraverse(root->rchild);
		}
}
void inordertraverse(rb_node_t* root)
{
	if(root != &nil)
	{

		inordertraverse(root->lchild);
		printf("%d  ",root->key);
		inordertraverse(root->rchild);
	}
}
rb_node_t* rb_create(int n, int arr[])
{
	rb_node_t* root;
	int i = 0;
	root = &nil;
	for(i = 0;i<n;i++)
	{
		root = rb_insert(root,arr[i]);
	}
  return root;
}
rb_node_t* rb_search(rb_node_t* root,int key)
{
	rb_node_t* nodes = NULL;
	if(root == &nil) return nodes;
	if(key == root->key)
		return root;
	if(key<root->key)
		nodes = rb_search(root->lchild,key);
	else
		nodes = rb_search(root->rchild,key);
	return nodes;
}
int main(void) {
	nil.color = BLACK;
    int arr[10] = {2,3,4,1,6,5,7,9,8};
    rb_node_t* root1 = rb_create(9,arr);
    inordertraverse(root1);
//    printf("%d",root1->lchild->key);
    printf("\n");
    rb_node_t* nodedele = rb_search(root1,4);
    if(nodedele!=NULL)
    {
    	root1 = rb_delete(root1,nodedele);
    }
    inordertraverse(root1);
	return EXIT_SUCCESS;
}
