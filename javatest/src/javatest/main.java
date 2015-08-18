package javatest;
import java.util.Scanner;
public class main {

	static int fibonacci(int n)
	{
		if(n == 1)
		{
	//		System.out.printf("%d  ",n-1);
			return n-1;
		}
		if(n == 2)
		{
	//		System.out.printf("%d  ",n-1);
			return n-1;
		}
		if(n>2)
			{
			   int temp = fibonacci(n-1)+fibonacci(n-2);
			//   System.out.printf("%d  ",temp);
			   return temp;
			}
		return 1;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
  /*     System.out.println("hello world");
       int i=10;
       int num = ++i;
       num = ++i;
       System.out.println(num); 
       System.out.println(i); */
/*		
		int x = 1;
		int y= 0;
		int z = 0;
		for(x=1;x<10;x++)
		{
			for(y=0;y<10;y++)
			{
				for(z=0;z<10;z++)
				{
					if(x*x*x+y*y*y+z*z*z==x*100+y*10+z)
						System.out.println(x*100+y*10+z);
				}
			}
		}
	}
*/
/*		Integer i1 = 200;
		Integer i2 = 200;
		if(i1==i2)
		{
			System.out.println("==");
		}
		else
		{
			System.out.println("!=");
		}
	*/
		/*
		Scanner scanner = new Scanner(System.in);
		int number = (int) (Math.random() * 10);
		int guess;
		do{
            System.out.print("guess the number(0-9):");
            guess = scanner.nextInt();
            if(guess > number)  System.out.printf("too large\n");
            else if(guess > number) System.out.printf("too large\n");
		}while(guess!=number);
		
		System.out.printf("game over!\n");
		*/
	/*	int x = 200;
		int y = 200;
		Integer wx = x;
		Integer wy = y;
		System.out.println(x == y);
		System.out.println(wx == wy);
		
		int[] arr1 = {1,2,3};
		int[] arr2 = arr1;
		arr2[1]=20;
		System.out.println(arr1[1]);
		*/
		
		int fn=0;
		int fn_1=1;
		int fn_2=0;
		Scanner scanner = new Scanner(System.in);
		System.out.print("input the number of count:");
		int count = scanner.nextInt();
		for(int n = 0;n<count;n++)
		{
			
			if(n==0)
			  System.out.printf("%d  ",0);
			else if (n==1)
			  System.out.printf("%d  ",1);
			else 
			{
				fn = fn_1 + fn_2;
				System.out.printf("%d  ",fn);
				fn_2 = fn_1;
				fn_1 = fn;
			}
		}
	
	   int test = fibonacci(10);
	   System.out.printf("%d  ",test);
	}	
	
}


