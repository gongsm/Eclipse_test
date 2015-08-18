package javatest;

public class CashCard {
	String number;
	int balance;
	int bonus;
//	final int testnum;
	CashCard(String number, int balance, int bonus){
	
		this.number = number;
		this.balance = balance;
		this.bonus = bonus;
		
	}
   void store(int money){
	   if(money>0){
		   this.balance +=money;
		   if(money>1000){
			   this.bonus++;
		   }
	   }
	   else{
		   System.out.println("the store monery is negative!!");
	   }
   }
   
   void charge(int money){
	   if(money>0){
		   if(money<this.balance){
			   this.balance -= money;
		   }
		   else{
			   System.out.println("balance is not enough!!");
		   }
	   }
	   else{
		   System.out.println("chanr money is negative!!");
	   }
   }

  

}

