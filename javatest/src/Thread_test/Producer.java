package Thread_test;

public class Producer implements Runnable{

    private Clerk clerk;
    
    public Producer(Clerk clerk){
 	   this.clerk = clerk;
    }
    
    public void run(){
 	   System.out.println("Producer start to produce data.....");
 	   for(int i=0;i<10;i++){
 		   try{
 			   Thread.sleep((int)(Math.random()*3000));
 		   }catch(InterruptedException ex){
 			   throw new RuntimeException(ex);
 		   }
 		clerk.setProduct(i);
 	   }
    }

}
