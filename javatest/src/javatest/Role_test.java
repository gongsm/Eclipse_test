package javatest;

public class Role_test {
	public static void swap(int a,int b){
		int temp = a;
		a = b;
		b = temp;
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
        SwordsMan man= new SwordsMan("snail",100,100);
        SwordsMan man2 = new SwordsMan();
        man2.setName("snail");
        System.out.printf("%s,%d,%d%n",man.getName(),man.getBlood(),man.getLevel());
      /*  man.showBlood(man);*/
       System.out.println(man);
       /* System.out.printf("%s", man.toString());*/
        System.out.println(man.equals(man2));
/*        int a = 9;
        int b = 10;
        swap(a,b);
        System.out.printf("%d,%d",a,b);
        int c = 9;
        int d = 9;
        System.out.println(c==d);*/
        
	}

}
