package interface_test;

public abstract class Fish implements Swimmer{
	protected String name;
	public Fish(String name){
		this.name = name;
	}
	public String getName(){
		return name;
	}
	
	public abstract void swim();
} 

 class  Shark extends Fish{
	public Shark(String name){
		super(name);
	}
	
	public void swim(){
		System.out.printf("shark %s swimming %n",name);
	}
}