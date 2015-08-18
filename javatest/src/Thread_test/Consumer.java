package Thread_test;

public class Consumer implements Runnable{
       private Clerk clerk;
       
       public Consumer(Clerk clerk){
    	   this.clerk = clerk;
       }
       
       public void run(){
    	   System.out.println("consumer start to consum data.....");
    	   for(int i=0;i<10;i++){
    		   try{
    			   Thread.sleep((int)(Math.random()*3000));
    		   }catch(InterruptedException ex){
    			   throw new RuntimeException(ex);
    		   }
    		   int product = clerk.getProduct();
    	   }
       }
}
