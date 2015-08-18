package javatest;

import javax.swing.text.html.HTMLDocument.HTMLReader.IsindexAction;

public abstract class Role {
	private String name;
	private int level;
	private int blood;
	Role(){
		System.out.print("role");
	}
	Role(String name,int level,int blood){
		System.out.print("in role");
		this.name = name;
		this.blood = blood;
		this.level = level;
	}
	public static void drawFight(Role role){
		System.out.print(role.getName());
		role.fight();
	}
	public static void showBlood(Role role){/*多态的使用，任何继承该类的子类都可通过传递子类本身调用该函数， 用于定义子类共同的行为，但各子类执行不同的操作*/
		System.out.printf("%s BLOOD(血量) %d%n", role.getName(),role.getBlood());
	}
	public int getBlood(){
	
		return this.blood;
	}
	public void setBlood(int blood){
	
		 this.blood = blood;
	}
	public String getName(){
		
		return this.name;
	}
	public void setName(String name){
	
		 this.name = name;
	}
    public int getLevel(){
		
		return this.level;
	}
	public void setLevel(int level){
	
		 this.level = level;
	}
    public String toString(){
    	return String.format("(%s,%d,%d)",this.name,this.blood,this.level);
    }
    public boolean equals(Object other){
    	if(this == other){
    		return true;
    	}
    	if(!(other instanceof Role)){
    		return false;
    	}
    	Role role = (Role) other;
    	if(getName().equals(role.getName())){
    		return true;
    	}
    	return false;
    }
	public abstract void fight();/*内涵抽象方法的类，一定要在class前标志abstract，abstract的类不能用来创建实例*/
}
