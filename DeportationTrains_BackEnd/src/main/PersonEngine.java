package main;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import com.google.gdata.client.authn.oauth.*;
import com.google.gdata.client.spreadsheet.*;
import com.google.gdata.data.*;
import com.google.gdata.data.batch.*;
import com.google.gdata.data.spreadsheet.*;
import com.google.gdata.util.*;

public class PersonEngine {

	public static void main (String []args) throws IOException, ServiceException{
		SpreadsheetService service = new SpreadsheetService("MySpreadsheetIntegration-v1");
		
		URL SPREADSHEET_FEED_URL = new URL("https://spreadsheets.google.com/feeds/spreadsheets/private/full");
		SpreadsheetFeed feed = service.getFeed(SPREADSHEET_FEED_URL, SpreadsheetFeed.class);
		List<SpreadsheetEntry> spreadsheets = feed.getEntries();
		
		if (spreadsheets.size() == 0) {
		      System.out.println("Nothing Found");
	    }
		
		SpreadsheetEntry spreadsheet = spreadsheets.get(0);
	    System.out.println(spreadsheet.getTitle().getPlainText());
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
