package main;

import java.util.ArrayList;

import com.google.gdata.client.authn.oauth.*;
import com.google.gdata.client.spreadsheet.*;
import com.google.gdata.data.*;
import com.google.gdata.data.batch.*;
import com.google.gdata.data.spreadsheet.*;
import com.google.gdata.util.*;

public class PersonEngine {

	public static void main (String []args){
		
	}
	
	//method to pull in data
	public ArrayList importData(){
		int number_people = 0;
		ArrayList<Person> people = new ArrayList<Person>();
		
		for (int i = 0; i < number_people; i++){
			//import one by one
			
			//add to end of array
		}
		
		return null;
	}
	
	
	//method to create person object
	private class Person {
		
		String caseFile;
		int doc;
		String name;
		String citizenship;
		String ethnicity;
		String sex;
		String birth;
		String occupation;
		String marriage;
		String imgRef;
		
	}
	
}
