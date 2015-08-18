//============================================================================
// Name        : test.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================
/*
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <Windows.h>
int main()
{
	FILE *file1 = fopen("test1.txt","wb");
	FILE *file2 = fopen("test2.txt","w");
	assert(file1 && file2);
	char str[1024] = "this is a test!\r\nyou know";//再把\n换成\r\n试试
	int len = strlen(str);
	int writeLen1 = fwrite(str, 1, len, file1);
	int writeLen2 = fprintf(file2, str);
	assert(writeLen1 == len && writeLen2 == len);
	fclose(file1);
	fclose(file2);

	printf("现在请打开test.txt文件看看，里面有没有换行,换任意键继续\n");
	system("pause");

	file1 = NULL;
	file2 = NULL;

	//现在我们在从文件里读取len个字节输出到控制台
	//下面的测试可以直接用ultraEdit或者winHex看其16进制是否是这几个字符，特别是'\n'
	char *str1[1024] = {0};
	char *str2[1024] = {0};
	file1 = fopen("test1.txt","rb");
	file2 = fopen("test2.txt","r");
	assert(file1 && file2);

	int readLen1 = fread(str1, 1, len, file1);


	assert(readLen1 == len);//判断读出的字节数与写入的是否相等



	printf("file1：\n");
	printf("%s",str1);


	return 0;
}

*/
#include<stdio.h>
#include<stdlib.h>
int main()
{
          char * p1;
          char * p2;
         int i=1;
          printf("%d\n",sizeof(char *));
         for(;i<100;i++)
         {
                 p1=NULL;
                 p2=NULL;
                 p1=(char *)malloc(i*sizeof(char));
                 p2=(char *)malloc(1*sizeof(char));
                 printf("i=%d     %d\n",i,(p2-p1));
         }
  //       getchar();
 }

