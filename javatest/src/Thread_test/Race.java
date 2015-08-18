package Thread_test;

public class Race {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
           Tortoise tor = new Tortoise(10);
           Hare hare = new Hare(10);
           Thread torThread = new Thread(tor);
           Thread hareThread = new Thread(hare);
           torThread.start();
           hareThread.start();
	}

}
