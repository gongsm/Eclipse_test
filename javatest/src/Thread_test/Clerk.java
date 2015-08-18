package Thread_test;

public class Clerk {
	private int product = -1;
	
	public synchronized void setProduct(int product){
		while(this.product!=-1){
			try{
				wait();
			}catch(InterruptedException ex){
				throw new RuntimeException(ex);
			}
		}
		this.product = product;
		System.out.printf("producer set %d%n", product);
		notify();
	}
	
	public synchronized int getProduct(){
		while(this.product==-1){
			try{
				wait();
			}catch(InterruptedException ex){
				throw new RuntimeException(ex);
			}
		}
		int p = this.product;
		System.out.printf("comsumer  get %d%n", p);
		this.product = -1;
		notify();
		return p;
	}

}
