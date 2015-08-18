package exception_test;
import java.util.*;
public class test {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
      
    	   Scanner scanner = new Scanner(System.in);
    	   double sum = 0;
    	   int count = 0;
    	   int number;
    	   System.out.printf("input int end with 0:%n"); 
    	   while(true){
    		   try{
    		   number = scanner.nextInt();
    		   if(number == 0){
    			   break;
    		   }
    		   sum +=number;
    		   count++;
    	   }catch(InputMismatchException ex){
        	   System.out.printf("miss the num:%s%n",scanner.next());
           }
    	  
       }
    	   System.out.printf("average:%.2f%n",sum/count); 
	}

}
