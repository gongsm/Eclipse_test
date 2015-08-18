package Collection_test;
import java.util.*;
public class Set_test {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
 /*        Scanner scanner = new Scanner(System.in);
         System.out.print("input words");
         String line = scanner.nextLine();
         String[] tokens = line.split(" ");
         Set words = new HashSet();
         for(String token:tokens){
        	 words.add(token);
         }
         System.out.printf("diff words num%d:%s%n", words.size(),words);*/
/*		Set<Integer> numbers = new TreeSet<>();
		numbers.add(1);
		numbers.add(4);
		numbers.add(1);
		numbers.add(3);
	//	foreach(numbers);
		for(Integer number:numbers){
			System.out.println(number);
		}
		*/
		
		Map<String, String> messages = new HashMap<>();
		messages.put("justin", "hello");
		messages.put("monica", "hihi");
		foreach(messages.values());
	}
  private static void foreach(Collection<String> numbers){
	  for(String number:numbers){
		  System.out.println(number);
	  }
  }
}
