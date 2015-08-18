package interface_test;

public class interface_test {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
         Swimmer swimmer1 = new Shark("snail");/*SharkÓµÓÐSwimmerÐÐÎª*/
         swimmer1.swim();
         Shark shark = (Shark) swimmer1;
         shark.getName();
         
	}

}
