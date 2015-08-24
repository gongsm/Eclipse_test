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
int main(void) {
	nil.color = BLACK;
    int arr[10] = {2,3,4,1,6,5,7,9,8};
    rb_node_t* root1 = rb_create(9,arr);
    printf("%d",root1->lchild->key);

	return EXIT_SUCCESS;
}
