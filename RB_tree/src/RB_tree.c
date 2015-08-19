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
rb_node_t* rb_rotate_left(rb_node_t* root,rb_node_t* node)
{
	rb_node_t* right = node->rchild;
	if(right == NULL) return root;
	if(node->rchild = right->lchild)
	{
		right->lchild->parent = node;
	}
    right->lchild = node;
    if(right->parent = node->parent)
    {
    	if(node->parent->lchild == node)
    	{
    		node->parent->lchild = right;
    	}
    	else
    	{
    		node->parent->rchild = right;
    	}
    }
    else
    	root = right;
    node->parent = right;
	return root;
}

rb_node_t* rb_rotate_right(rb_node_t* root,rb_node_t* node)
{
	rb_node_t* left = node->lchild;
	if(left == NULL) return root;
	if(node->lchild = left->rchild)
	{
		left->rchild->parent = node;
	}

	left->rchild = node;
	if(left->parent = node->parent)
	{
		if(node->parent->lchild == node)
		{
			node->parent->lchild = left;
		}
		else
		{
			node->parent->rchild = left;
		}
	}
	else root = left;
	node->parent = left;

	return root;
}

rb_node_t* rb_insert(rb_node_t* root, int key)
{
	rb_node_t* node = rb_newnode(key);

	return root;
}
int main(void) {
	nil.color = BLACK;



	return EXIT_SUCCESS;
}
