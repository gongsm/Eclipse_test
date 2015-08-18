package Thread_test;

public class ProducerComsumerDemo {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
         Clerk clerk = new Clerk();
         new Thread(new Producer(clerk)).start();
         new Thread(new Consumer(clerk)).start();
	}

}
