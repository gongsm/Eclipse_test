package javatest;

public class some {

	private int x;
	public some(){
		this(10);
		System.out.println("some()");
		
	}
	public some(int x){
		this.x = x;
	}
	int getvalue(){
		return this.x;
	}
	public static int sum(int ... numbers){
		int sum= 0;
		for(int i=0;i<numbers.length;i++){
			sum +=numbers[i];
		}
		return sum;
	}
	void doServer(){
		System.out.println("some server");
	}
}


class other extends some{
	void doServer(){
		System.out.println("other server");
	}
}