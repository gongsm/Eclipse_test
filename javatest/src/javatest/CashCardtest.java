package javatest;

public class CashCardtest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
         CashCard[] cards ={
        		 new CashCard("A001", 500, 0),
        		 new CashCard("A002", 1500, 0),
        		 new CashCard("A003", 2500, 0)
         };
         
         for(CashCard card: cards){
        	 System.out.printf("for (%s,%d,%d) store:1000%n",card.number,card.balance,card.bonus);
        	 card.store(1000);
        	 System.out.printf("(%s,%d,%d)%n",card.number,card.balance,card.bonus);
         }
         
         
         
    }
         
         
}


