package javatest;
/*ºÃ≥–”Î∂‡Ã¨*/
public class SwordsMan extends Role{
	SwordsMan(){
		System.out.print("in SwordsMan");
	}
	SwordsMan(String name,int level,int blood){
		super( name, level, blood);
		System.out.print("in SwordsMan");
	}
	public void fight(){
		System.out.println("attact with sword!");
	}
	public String toString(){
		return "SwordsMan" + super.toString();
	}
}
