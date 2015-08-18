package Thread_test;

class Variable {
	/*volatile*/ static int i=0,j=0;
	static synchronized void one(){i++;j++;}
	static synchronized void two(){
		System.out.printf("i = %d,j =%d%n", i,j);
	}
}
public class volatile_test {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
        Thread t1 = new Thread(){
        	public void run(){
        		while(true){
        			Variable.one();
        		}
        	}
        };
        Thread t2 = new Thread(){
        	public void run(){
        		while(true){
        			Variable.two();
        		}
        	}
        };
        t1.start();
        t2.start();
	}

}
