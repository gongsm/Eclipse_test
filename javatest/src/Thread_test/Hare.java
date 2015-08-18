package Thread_test;

public class Hare implements Runnable{
	
	private boolean[] flags = {true,false};
	private int totalStep;
	private int step;
	public Hare(int totalstep){
		this.totalStep = totalstep;
	}
	
	@Override
	public void run(){
		try {
			while(step<totalStep){
				Thread.sleep(1000);
				boolean isHareSleep = flags[((int)(Math.random()*10))%2];
				if(isHareSleep){
					System.out.println("hare sleep zzzzz");
				}
				else{
					step += 2;
					System.out.printf("hare run %d step...%n", step);
				}
				
			}
		}catch(InterruptedException ex){
			throw new RuntimeException(ex);
		}
	}

}
