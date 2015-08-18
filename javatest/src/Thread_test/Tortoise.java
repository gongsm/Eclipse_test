package Thread_test;



public class Tortoise implements Runnable{
	
	private int totalStep;
	private int step;
	public Tortoise(int totalstep){
		this.totalStep = totalstep;
	}
	
	@Override
	public void run(){
		try {
			while(step<totalStep){
				Thread.sleep(1000);
				step++;
				System.out.printf("tortoise run %d step...%n", step);
			}
		}catch(InterruptedException ex){
			throw new RuntimeException(ex);
		}
	}

}


