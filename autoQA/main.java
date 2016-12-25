package zfh;
import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.Segment;
import com.hankcs.hanlp.seg.common.Term;
import com.hankcs.hanlp.suggest.Suggester;
import java.util.List;
import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLSentence;
import com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLWord;

public class Readfile {
	static int count = 0;
	static int zzz = 0;
	static Segment segment = HanLP.newSegment().enableAllNamedEntityRecognize(true);
	static ArrayList<String> strs = new ArrayList<String>();
	static String query_orig = "";
	static String query_type ="";
	static String true_answer = "";
	static ArrayList<String> Country = new ArrayList<String>();
	static ArrayList<String> Capital = new ArrayList<String>();
	static ArrayList<String> City = new ArrayList<String>();
	static FileWriter fw;
    public static void readTxtFile(String filePath){
        try {
                String encoding="UTF-8";
                File capital = new File("G:\\java_workspace\\WebDataMining\\src\\capital.txt");
                if(capital.isFile() && capital.exists()){ //判断文件是否存在
                    InputStreamReader read = new InputStreamReader(
                    new FileInputStream(capital),encoding);//考虑到编码格式
                    BufferedReader bufferedReader = new BufferedReader(read);
                    String line = null;
                    while((line = bufferedReader.readLine()) != null){
                        Country.add(getStrings(line,"^(.+?)\\t.*$").get(0));
                        Capital.add(getStrings(line,"^.*\\t(.+?)$").get(0));
                    }
                    read.close();
                }    
                File city = new File("G:\\java_workspace\\WebDataMining\\src\\City.txt");
                if(city.isFile() && city.exists()){ //判断文件是否存在
                    InputStreamReader read = new InputStreamReader(
                    new FileInputStream(city),encoding);//考虑到编码格式
                    BufferedReader bufferedReader = new BufferedReader(read);
                    String line = null;
                    while((line = bufferedReader.readLine()) != null){
                    	
                    	ArrayList<String> cityarr = getStrings(line,"([\u4e00-\u9fa5]+)");
                    	for (String ss:cityarr){
                        City.add(ss);
                    	}
                    }
                    //System.out.println(City);
                    read.close();
                }
                fw=new FileWriter("G:\\java_workspace\\WebDataMining\\src\\final\\result\\zfh_2_15.txt");
                File file=new File(filePath);
                if(file.isFile() && file.exists()){ //判断文件是否存在
                    InputStreamReader read = new InputStreamReader(
                    new FileInputStream(file),encoding);//考虑到编码格式
                    BufferedReader bufferedReader = new BufferedReader(read);
                    String line1 = null;
                    String line2 = null;
                    while((line1 = bufferedReader.readLine()) != null){
                        //System.out.println(line1);
                    	if(line1.matches("\\{.*\\}")==false){
                        	//fw.write(line2);
                        	continue;
                        }
                    	String iid = getStrings(line1, "\\'id\':\\s\\'(.*?)\\'").get(0);
                    	
                    	System.out.println(iid);
                    	int iii = Integer.parseInt(iid);    
                    	if(iii==4873) continue;
                    	line2 = bufferedReader.readLine();
                    	//if(iii<660) continue;
                    	try{
                    	fw.write("\n"+iid+"\t");
                    	}
                    	catch (Exception e) {
                            System.out.println("写文件出错");
                            e.printStackTrace();
                        }
                        
                        if(line2.length()<1) continue;
                        if(line2.matches("\\[.*\\]")==false){
                        	fw.write(line2);
                        	continue;
                        }
                        
                        //if(zzz<1200) continue;
                    	//if(zzz >= 3633) break;
                        //System.out.println(line2);
                        query_proc(line1,0);
                        query_proc(line2,1);
                    }
                    read.close();
                    fw.flush();
                    fw.close();
                }
                else{
                		System.out.println("找不到指定的文件");
                }
        } catch (Exception e) {
            System.out.println("读取文件内容出错");
            e.printStackTrace();
        }
    }
    private static ArrayList<String> getStrings(String str, String pt) {
        Pattern p = Pattern.compile(pt);
        Matcher m = p.matcher(str);
        ArrayList<String> strs = new ArrayList<String>();
        while (m.find()) {
            strs.add(m.group(1));            
        } 
        return strs;
        //for (String s : strs){
        //    System.out.println(s);
        //}        
    }
    public static void query_proc(String query, int mode){
    	if(mode==0){

    	strs = getStrings(query, "\\'content\':\\s\\'(.*?)\\'");
    	for(String s: strs){
    		query_orig = s;
    	}
    	query_type = query_classifier(query_orig);
    	//System.out.println(query_type);
    	//if(query_type!="Unknown"){
    	//	count = count + 1;
    	//}
    	strs = getStrings(query,"\\'true_answer\':\\s\\'(.*?)\\'"); 
    	for(String s: strs){
    		true_answer = s;
    	}   
    	//System.out.println(query_orig);
    	//System.out.println(true_answer);
    	}
    	else if(mode==1){
    		try{
    	strs = getStrings(query,"\\([01]\\.\\d+,\\s\\'(.*?)\\'"); 
    		
            } 
    		catch (Exception e) {
                System.out.println("读取文件内容出错"+query);
                e.printStackTrace();
            }
    	ArrayList<String> keywords = new ArrayList<String>();
    	keywords = getStrings(query,"\\',\\s\\'(.+?)\\'"); 
    	//strs1 = getStrings(query,"\\(([01]\\.\\d.+?),\\s\\'.*?\\'"); 
    	//int cand_count = strs.size();
    	//for(int i = 0; i < cand_count; i = i + 1){
    		//System.out.println(strs.get(i));
    		//System.out.println(strs1.get(i));
    	//}
    	//System.out.println();
    	Answer_main(query_orig,query_type,strs,keywords,true_answer);
    	}
    	
    }
    public static void Answer_main(String query, String ans_type, ArrayList<String> cand, ArrayList<String> keywords, String true_answer){
    	if(ans_type=="Unknown") Unknown_query_main(query, cand, keywords, true_answer);
    	
    	else{
    	int find = 0;
    	String answer = "";
    	//System.out.println("问题："+query);
    	//System.out.println("正确答案："+true_answer);
    	if(ans_type.equals("Dynasty")){
    		Answer_Retrieval1 ar = new Answer_Retrieval1();
    		count = count + ar.Answer_dynasty(query, ans_type, cand, keywords, true_answer);
    		
    	}
    	if(ans_type.equals("Capital")){
    		for(int co=0;co<Country.size();co = co + 1){
    			if(query.indexOf(Country.get(co))>=0){
    				answer = Capital.get(co);
    				find = 1;
    				break;
    			}
    		}
    		for(int co=0;co<Capital.size();co = co + 1){
    			if(query.indexOf(Capital.get(co))>=0){
    				answer = Country.get(co);
    				find = 1;
    				break;
    			}
    		}
    		if(find==1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
    	    	
	    		if(answer.equals(true_answer)){
	    			count = count + 1;
	    		}
	    		
    		}
    	}
    	if(ans_type.equals("Name")){
        	int cand_count = cand.size();
	    	for(int tmp0 = 0; tmp0<cand_count; tmp0 = tmp0 + 1){
	    		String sentence = cand.get(tmp0);
	    		if(keywords.size()<=tmp0) continue;
	    		String key = keywords.get(tmp0);
	    		//System.out.println(key);
	    		//System.out.println(query);
	    	    String key_type = segment.seg(key).get(0).nature.toString();
    			if(query.indexOf(key)<0 &&(key_type == "nr"||key_type == "nr1"||key_type == "nr2"||key_type == "nrf"||key_type == "nrj")){	    	    
    			//if(query.indexOf(key)<0 && segment.seg(key).size()==1&&(key_type == "nr"||key_type == "nr1"||key_type == "nr2"||key_type == "nrf"||key_type == "nrj")){
    				//answer = segment.seg(key).get(0).word;
    				answer = segment.seg(key).get(0).word;
    				find = 1;
    				break;
    			}
	    		List<Term> termList = segment.seg(sentence);
	    		for(Term t:termList){
	    			String type_word = t.nature.toString();
	    			if(query.indexOf(t.word)<0&&(type_word == "nr"||type_word == "nr1"||type_word == "nr2"||type_word == "nrf"||type_word == "nrj")){
	    				find = 1;
	    				answer = t.word;
	    				break;
	    			}
	    		}
	    		if(find == 1) break;
	    	}
	    	if(find == 1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
	    		if(answer.equals(true_answer)){
	    			count = count + 1;
	    		}
	    	}
    	}
    	/***************国家************/
    	if(ans_type.equals("Country")){
    		for(String key: keywords){
    			for(String cc:Country){
    				if(key.indexOf(cc)>=0){
    					if(query.indexOf(cc)>=0) continue;//去重
    					find = 1;
    					answer = cc;
    					break;   					
    				}
    			}
    			if(find == 1) break;
    		}
    		if(find==0){
	    	for(String sentence: cand){
	    		List<Term> termList = segment.seg(sentence);
	    		for(Term t:termList){
	    			//String type_word = t.nature.toString();
	    			for(String cc:Country){
	    				if(t.word.indexOf(cc)>=0) {
	    					if(query.indexOf(cc)>=0) continue;//去重
	    					find = 1;
	    					answer = cc;
	    					break;
	    				}
	    		}
	    		if(find == 1) break;
	    	}
	    	}	
	    	}
	    	if(find == 1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
	    		if(answer.equals(true_answer)){
	    			count = count + 1;
	    		}
    	}
    	}
    	/***************年************/
    	if(ans_type.equals("Year_Number")){
	    	for(String sentence: cand){
	    		List<Term> termList = segment.seg(sentence);
	    		int term_number = termList.size();
	    		for(int tmp = 0; tmp < term_number; tmp = tmp + 1){
	    			Term t = termList.get(tmp);
	    			String term_word = t.word;
	    			String type_word = t.nature.toString();
	    			if(term_word.matches(".*年.*")){
	    				if(tmp > 0){
	    					Term year_get = termList.get(tmp-1);
	    					answer = year_get.word;
	    					if(query.indexOf(year_get.word)>=0) continue;//排除答案已在问题中出现的情况
	    					find = 1;
	    					break;
	    				}
	    			}
	    		}
	    		if(find == 1) break;
	    	}
	    	if(find == 1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
	    		if(answer.equals(true_answer)){
	    			count = count + 1;
	    		}
	    	}
    	}
    	/***************多少年************/
    	if(ans_type.equals("Year_Count")){
	    	for(String sentence: cand){
	    		List<Term> termList = segment.seg(sentence);
	    		int term_number = termList.size();
	    		for(int tmp = 0; tmp < term_number; tmp = tmp + 1){
	    			Term t = termList.get(tmp);
	    			String term_word = t.word;
	    			
	    			if(term_word.matches(".*年.*")){
	    				if(tmp > 0){
	    					Term year_get = termList.get(tmp-1);
	    					answer = year_get.word;
	    					if(query.indexOf(year_get.word)>=0) continue;//排除答案已在问题中出现的情况
	    					find = 1;
	    					break;
	    				}
	    			}
	    		}
	    		if(find == 1) break;
	    	}
	    	if(find == 1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
	    		if(answer.equals(true_answer)){
	    			count = count + 1;
	    		}
	    	}
    	}
    	/***************月************/
    	if(ans_type.equals("Month")){
	    	for(String sentence: cand){
	    		List<Term> termList = segment.seg(sentence);
	    		int term_number = termList.size();
	    		for(int tmp = 0; tmp < term_number; tmp = tmp + 1){
	    			Term t = termList.get(tmp);
	    			String term_word = t.word;
	    			String type_word = t.nature.toString();
	    			if(term_word.matches(".*月.*")){
	    				if(tmp > 0){
	    					Term year_get = termList.get(tmp-1);
	    					answer = year_get.word;
	    					find = 1;
	    					break;
	    				}
	    			}
	    		}
	    		if(find == 1) break;
	    	}
	    	if(find == 1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
	    		if(answer.equals(true_answer)){
	    			count = count + 1;
	    		}
	    	}
    	}
    	/***************颜色************/
    	if(ans_type.equals("Color")){
    		Answer_Retrieval1 ar = new Answer_Retrieval1();
    		count = count + ar.Answer_color(query, ans_type, cand, keywords, true_answer);
    		
    	}
    	/***************省************/
    	if(ans_type.equals("Province")){
    		Answer_Retrieval1 ar = new Answer_Retrieval1();
    		count = count + ar.Answer_province(query, ans_type, cand, keywords, true_answer);
    		
    	}   
    	/***************市************/
    	if(ans_type.equals("City")){
        	int cand_count = cand.size();
        	for(int tmp0 = 0; tmp0<cand_count; tmp0 = tmp0 + 1){
        		String sentence = cand.get(tmp0);
        		String key = keywords.get(tmp0);
        		for(String cc : City){
        			if(key.indexOf(cc)>=0){
        				if(query.indexOf(cc)<0){
        				find = 1;
        				answer = cc;
        				break;
        				}
        			}
        		}
            	if(find == 1) break;		
        		List<Term> termList = segment.seg(sentence);
        		for(Term t:termList){
        			String word = t.word;
            		for(String cc : City){
            			if(word.indexOf(cc)>=0){
            				if(query.indexOf(cc)<0){
            				find = 1;
            				answer = cc;
            				break;
            				}
            			}
            		}
            		if(find==1) break;
        		}
        		if(find == 1) break;
        	}
        	if(find == 1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
        		if(answer.equals(true_answer)){
        			count = count + 1;
        		}
        	}
        	else{
        		Answer_Retrieval1 ar= new Answer_Retrieval1();
        		count = count + ar.Answer_city(query, ans_type, cand, keywords, true_answer);
        	}
    	}   
    	/***************日************/
    	if(ans_type.equals("Day")){
        	int query_flag = 4;
        	if(query.matches(".*月.*")) query_flag = 1;
        	else if(query.matches(".*年.*")) query_flag = 2;
        	else if(query.matches(".*日是.*")||query.matches(".*节.*")) query_flag = 3;
        	if(query_flag==1){//第一种情况，问某月几号，直接提取日之前的信息
	    	for(String sentence: cand){
	    		List<Term> termList = segment.seg(sentence);
	    		int term_number = termList.size();
	    		for(int tmp = 0; tmp < term_number; tmp = tmp + 1){
	    			Term t = termList.get(tmp);
	    			String term_word = t.word;
	    			String type_word = t.nature.toString();
	    			if(term_word.matches(".*日.*")){
	    				if(tmp > 0){
	    					Term year_get = termList.get(tmp-1);
	    					answer = year_get.word;
	    					find = 1;
	    					break;
	    				}
	    			}
	    			if(term_word.matches(".*号.*")){
	    				if(tmp > 0){
	    					Term year_get = termList.get(tmp-1);
	    					answer = year_get.word;
	    					find = 1;
	    					break;
	    				}
	    			}
	    		}
	    		if(find == 1) break;
	    	}
        	}
        	else if(query_flag==2||query_flag==3){//第二种情况，问某年几号，给出月和日
	    	for(String sentence: cand){
	    		//System.out.println("当前句子"+sentence);
	    		if(sentence.matches(".*月.+日.*")==true){
		    		find = 1;
		    		String month_tmp = "";
		    		if(sentence.matches(".*(\\d+)月.*")){
		    			month_tmp  = getStrings(sentence,".*(\\d+?)月.*").get(0); 
		    		}
		    		else if(sentence.matches(".*([\\u4e00-\\u9fa5])月.*")){
		    			month_tmp  = getStrings(sentence,".*([\\u4e00-\\u9fa5])月.*").get(0); 
		    		}
		    		String day_tmp = getStrings(sentence,".*月(.+?)日.*").get(0); 
		    		answer = month_tmp + "月" + day_tmp + "日";
		    		break;
	    			}
	    		}
        	}
        	
	    	else{
	    		for(String sentence: cand){
	    			if(sentence.matches(".*年.*月.*日.*")){
	    				find = 1;
	    				String year_tmp = getStrings(sentence,".*(\\d+)年.*").get(0);
	    				String month_tmp = "五";
	    				if(getStrings(sentence,".*(\\d+)月.*").size()>0) month_tmp = getStrings(sentence,".*(\\d+)月.*").get(0); 
	    				String day_tmp = getStrings(sentence,".*(\\d+)日.*").get(0); 
	    				answer = year_tmp + "年" + month_tmp + "月" + day_tmp + "日";
	    				break;
	    			}
	    		}		
	    	}
	    	if(find == 1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
	    		if(answer.equals(true_answer)){
	    			count = count + 1;
	    		}
	    	}
	    	//else System.out.println("N/A");
    	}
    	
    	/*****************数量*****************/
    	
    	if(ans_type.equals("Count")){
        	int cand_count = cand.size();
        	WordJudge wj = new WordJudge();
        	if(wj.countjudge(query)==1){
    	    	for(int tmp0 = 0; tmp0<cand_count; tmp0 = tmp0 + 1){
    	    		String sentence = cand.get(tmp0);
    	    		String key = keywords.get(tmp0);
    	    		//System.out.println(key);
    	    		//System.out.println(query);
    	    		if(key.matches(".*第.*")){
    	    			List<Term> termList = segment.seg(key);
    	    			for(int tmpp = 0;tmpp<termList.size();tmpp = tmpp + 1){
    	    				Term t = termList.get(tmpp);
    	    				if(t.word=="第"&&termList.get(tmpp+1).nature.toString()=="m"){
    	    					find = 1;
    	    					answer = termList.get(tmpp+1).word;
    	    					break;
    	    				}
    	    			}
    	    			if(find==1) {
    	        	    	try{
    	        	        	fw.write(answer);
    	        	        	}
    	        	        	catch (Exception e) {
    	        	                System.out.println("写文件出错");
    	        	                e.printStackTrace();
    	        	            }
    	    	    		if(answer.equals(true_answer)){
    	    	    			count = count + 1;
    	    	    		}
    	    	    		return;
    	    			}	
    	    		}
    	    		if(sentence.matches(".*第.*")){
    	    			List<Term> termList = segment.seg(sentence);
    	    			for(int tmpp = 0;tmpp<termList.size();tmpp = tmpp + 1){
    	    				Term t = termList.get(tmpp);
    	    				if(t.word.matches("第.*")){
    	    					find = 1;
    	    					answer = t.word.substring(1, t.word.length());
    	    					break;
    	    				}
    	    				else if(t.word=="第"&&termList.get(tmpp+1).nature.toString()=="m"){
    	    					find = 1;
    	    					answer = termList.get(tmpp+1).word;
    	    					break;
    	    				}
    	    			}
    	    			if(find==1) {
    	        	    	try{
    	        	        	fw.write(answer);
    	        	        	}
    	        	        	catch (Exception e) {
    	        	                System.out.println("写文件出错");
    	        	                e.printStackTrace();
    	        	            }
    	    	    		if(answer.equals(true_answer)){
    	    	    			count = count + 1;
    	    	    		}
    	    	    		return;
    	    			}	
    	    		}
    	    	}
        	}
        	else if(wj.countjudge(query)==2){
        		String query_type_1 = "";
        		List<Term> termList = segment.seg(query);
        		for(int tmpp = 0; tmpp < termList.size(); tmpp = tmpp + 1){
        			if(termList.get(tmpp).word=="是"||termList.get(tmpp).word=="为"||termList.get(tmpp).word=="有"){
        				CoNLLSentence sentence = HanLP.parseDependency(query);
        		    	CoNLLWord[] wordArray = sentence.getWordArray();
        		        for (int i = 0; i <  wordArray.length; i++){
        		        	if(wordArray[i].DEPREL=="主谓关系"&&wordArray[i].HEAD.LEMMA==termList.get(tmpp).word){
        		        		query_type_1 = wordArray[i].LEMMA;
        		        		break;
        		        	}
        		        }
        			}
        		}
    	    	for(int tmp0 = 0; tmp0 < cand_count; tmp0 = tmp0 + 1){
    	    		String sentence = cand.get(tmp0);
    	    		if(sentence.matches(".*"+ query_type_1 + ".*")){
    	    			termList = segment.seg(sentence);
    	    			for(int tmpp = 0; tmpp < termList.size(); tmpp = tmpp + 1){
    	        			if(termList.get(tmpp).nature.toString()=="m"&&((tmpp==termList.size()-1)||((tmpp<termList.size()-1)&&wj.nyrjudge(termList.get(tmpp+1).word)==false))){
    	        				find = 1;
    	        				answer = termList.get(tmpp).word;
    	        				break;
    	        			}	
    	    			}
    	    		}
    	    		if(find==1){
    	    	    	try{
    	    	        	fw.write(answer);
    	    	        	}
    	    	        	catch (Exception e) {
    	    	                System.out.println("写文件出错");
    	    	                e.printStackTrace();
    	    	            }
	    	    		if(answer.equals(true_answer)){
	    	    			count = count + 1;
	    	    		}
	    	    		return;
    	    		}
    	    	}	
        	}
 //////333
        	else if(wj.countjudge(query)==3||wj.countjudge(query)==4){
        		String query_type_1 = "";
        		List<Term> termList = segment.seg(query);
        		for(int tmpp = 0; tmpp < termList.size(); tmpp = tmpp + 1){
        			if(termList.get(tmpp).word=="个"||termList.get(tmpp).word=="多少"){
        				CoNLLSentence sentence = HanLP.parseDependency(query);
        		    	CoNLLWord[] wordArray = sentence.getWordArray();
        		        for (int i = 0; i <  wordArray.length; i++){
        		        	if(wordArray[i].DEPREL=="定中关系"&&wordArray[i].LEMMA==termList.get(tmpp).word){
        		        		query_type_1 = wordArray[i].HEAD.LEMMA;
        		        		break;
        		        	}
        		        }
        			}
        		}
    	    	for(int tmp0 = 0; tmp0 < cand_count; tmp0 = tmp0 + 1){
    	    		String sentence = cand.get(tmp0);
    	    		if(sentence.matches(".*"+ query_type_1 + ".*")){
    	    			termList = segment.seg(sentence);
    	    			for(int tmpp = 0; tmpp < termList.size(); tmpp = tmpp + 1){
    	    				if(termList.get(tmpp).nature.toString()=="m"&&((tmpp==termList.size()-1)||((tmpp<termList.size()-1)&&wj.nyrjudge(termList.get(tmpp+1).word)==false))){
    	        				find = 1;
    	        				answer = termList.get(tmpp).word;
    	        				break;
    	        			}	
    	    			}
    	    		}
    	    		if(find==1){
    	    	    	try{
    	    	        	fw.write(answer);
    	    	        	}
    	    	        	catch (Exception e) {
    	    	                System.out.println("写文件出错");
    	    	                e.printStackTrace();
    	    	            }
	    	    		if(answer.equals(true_answer)){
	    	    			count = count + 1;
	    	    		}
	    	    		return;
    	    		}
    	    	}	
        	}
        	///555//////////////////////////////////
        	else if(wj.countjudge(query)==3||wj.countjudge(query)==4){
        		String query_type_1 = "";
        		List<Term> termList = segment.seg(query);
        		for(int tmpp = 0; tmpp < termList.size(); tmpp = tmpp + 1){
        			if(termList.get(tmpp).word=="几"){
        				CoNLLSentence sentence = HanLP.parseDependency(query);
        		    	CoNLLWord[] wordArray = sentence.getWordArray();
        		        for (int i = 0; i <  wordArray.length; i++){
        		        	if(wordArray[i].DEPREL=="定中关系"&&wordArray[i].LEMMA==termList.get(tmpp).word){
        		        		query_type_1 = wordArray[i].HEAD.LEMMA;
        		        		break;
        		        	}
        		        }
        			}
        		}
    	    	for(int tmp0 = 0; tmp0 < cand_count; tmp0 = tmp0 + 1){
    	    		String sentence = cand.get(tmp0);
    	    		if(sentence.matches(".*"+ query_type_1 + ".*")){
    	    			termList = segment.seg(sentence);
    	    			for(int tmpp = 0; tmpp < termList.size(); tmpp = tmpp + 1){
    	    				if(termList.get(tmpp).nature.toString()=="m"&&((tmpp==termList.size()-1)||((tmpp<termList.size()-1)&&wj.nyrjudge(termList.get(tmpp+1).word)==false))){
    	        				find = 1;
    	        				answer = termList.get(tmpp).word;
    	        				break;
    	        			}	
    	    			}
    	    		}
    	    		if(find==1){
    	    	    	try{
    	    	        	fw.write(answer);
    	    	        	}
    	    	        	catch (Exception e) {
    	    	                System.out.println("写文件出错");
    	    	                e.printStackTrace();
    	    	            }
	    	    		if(answer.equals(true_answer)){
	    	    			count = count + 1;
	    	    		}
	    	    		return;
    	    		}
    	    	}	
        	}
        	
        	else{
    	    	for(int tmp0 = 0; tmp0 < cand_count; tmp0 = tmp0 + 1){
    	    		String sentence = cand.get(tmp0);
	    			List<Term> termList = segment.seg(sentence);
	    			for(int tmpp = 0; tmpp < termList.size(); tmpp = tmpp + 1){
	    				if(termList.get(tmpp).nature.toString()=="m"&&((tmpp==termList.size()-1)||((tmpp<termList.size()-1)&&wj.nyrjudge(termList.get(tmpp+1).word)==false))){
	        				find = 1;
	        				answer = termList.get(tmpp).word;
	        				break;
	        			}	
	    			}
    	    		if(find==1){
    	    	    	try{
    	    	        	fw.write(answer);
    	    	        	}
    	    	        	catch (Exception e) {
    	    	                System.out.println("写文件出错");
    	    	                e.printStackTrace();
    	    	            }
        	    		if(answer.equals(true_answer)){
        	    			count = count + 1;
        	    		}
        	    		return;
    	    		}
    	    	}	
        	}
        	if(find==0){
    	    	for(int tmp0 = 0; tmp0 < cand_count; tmp0 = tmp0 + 1){
    	    		String sentence = cand.get(tmp0);
	    			List<Term> termList = segment.seg(sentence);
	    			for(int tmpp = 0; tmpp < termList.size(); tmpp = tmpp + 1){
	    				if(termList.get(tmpp).nature.toString()=="m"&&((tmpp==termList.size()-1)||((tmpp<termList.size()-1)&&wj.nyrjudge(termList.get(tmpp+1).word)==false))){
	        				find = 1;
	        				answer = termList.get(tmpp).word;
	        				break;
	        			}	
	    			}
    	    		if(find==1){
    	    	    	try{
    	    	        	fw.write(answer);
    	    	        	}
    	    	        	catch (Exception e) {
    	    	                System.out.println("写文件出错");
    	    	                e.printStackTrace();
    	    	            }
        	    		if(answer.equals(true_answer)){
        	    			count = count + 1;
        	    		}
        	    		return;
    	    		}
    	    	}
        	}
    	}
    }
    }
	public static boolean iscountry(String ic){
		for(String cc:Country){
			if(ic.indexOf(cc)>=0) return true;
		}
		return false;
	}
	public static boolean iscapital(String ic){
		for(String cc:Capital){
			if(ic.indexOf(cc)>=0) return true;
		}
		return false;
	}
	public static boolean iscity(String ic){
		for(String cc:City){
			if(ic.indexOf(cc)>=0) return true;
		}
		return false;
	}
    public static void Unknown_query_main(String query, ArrayList<String> cand, ArrayList<String> keywords, String true_answer){
    	CoNLLSentence query_c = HanLP.parseDependency(query);
    	String answer = "";
    	//System.out.println(query);
    	//System.out.println("正确答案是："+true_answer);
    	int find = 0;
    	ArrayList<String> subject_arr = new ArrayList<String>();
    	ArrayList<String> object_arr = new ArrayList<String>();
    	String query_main = "";
    	/*
        for (CoNLLWord word : query_c){
            System.out.printf("%s --(%s)--> %s\n", word.LEMMA, word.DEPREL, word.HEAD.LEMMA);
        }   
        */ 	
        for (CoNLLWord word : query_c){
            //System.out.printf("%s --(%s)--> %s\n", word.LEMMA, word.DEPREL, word.HEAD.LEMMA);
            if(word.DEPREL.equals("核心关系")) {query_main = word.LEMMA;break;}
        }
        for (CoNLLWord word : query_c){
            //System.out.printf("%s --(%s)--> %s\n", word.LEMMA, word.DEPREL, word.HEAD.LEMMA);
            if(word.HEAD.LEMMA.equals(query_main)   &&(word.DEPREL.equals("主谓关系")  )) {
            	subject_arr.add(word.LEMMA);
            }
            if(word.HEAD.LEMMA == query_main && (word.DEPREL.equals("动宾关系")||word.DEPREL.equals("间宾关系")||word.DEPREL.equals("介宾关系"))){
            	object_arr.add(word.LEMMA);
            }
        }
        for (String sentence: cand){
        	String sentence_main = "";
        	CoNLLSentence sentence_c = HanLP.parseDependency(sentence);
        	ArrayList<String> subject_sen = new ArrayList<String>();
        	ArrayList<String> object_sen = new ArrayList<String>();
            for (CoNLLWord word : query_c){
                //System.out.printf("%s --(%s)--> %s\n", word.LEMMA, word.DEPREL, word.HEAD.LEMMA);
                if(word.DEPREL.equals("核心关系")) {sentence_main = word.LEMMA;break;}
            }
            if(sentence_main.equals(query_main)==false) continue;
            for (CoNLLWord word : sentence_c){
                //System.out.printf("%s --(%s)--> %s\n", word.LEMMA, word.DEPREL, word.HEAD.LEMMA);
                if(word.HEAD.LEMMA.equals(query_main) &&(word.DEPREL.equals("主谓关系") )) {
                	subject_sen.add(word.LEMMA);
                }
                if(word.HEAD.LEMMA.equals(query_main)  && (word.DEPREL.equals("动宾关系") ||word.DEPREL.equals("间宾关系") ||word.DEPREL.equals("介宾关系") )){
                	object_sen.add(word.LEMMA);
                }
            }
            for(String sub_que: subject_arr){
            	for(String ob_sen:object_sen){
            		if(sub_que.equals(ob_sen)){
            			if(subject_sen.size()>0)
            			answer = subject_sen.get(0);
            			/*
            			if(answer.equals(true_answer)){
            				find = 1;
            				break;
            			}
            			*/
            			find = 1;
            			break;
            		}
            	}
            	if(find==1) break;
            }
            if(find==1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
            	if(answer.equals(true_answer)) count = count + 1;
            	break;
            }
            for(String ob_que: object_arr){
            	for(String ob_sen:object_sen){
            		if(ob_que.equals(ob_sen)){
            			if(subject_sen.size()>0)
            			answer = subject_sen.get(0);
            			/*
            			if(answer.equals(true_answer)){
            				find = 1;
            				break;
            			}
            			*/
            			find = 1;
            			break;
            		}
            	}
            	if(find==1) break;
            }           
            if(find==1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
            	if(answer.equals(true_answer)) count = count + 1;
            	break;
            }
            for(String sub_que: subject_arr){
            	for(String sub_sen:subject_sen){
            		if(sub_que.equals(sub_sen)){
            			if(object_sen.size()>0)
            			answer = object_sen.get(0);
            			/*
            			if(answer.equals(true_answer)){
            				find = 1;
            				break;
            			}
            			*/
            			find = 1;
            			break;
            		}
            	}
            	if(find==1) break;
            }           
            if(find==1){
    	    	try{
    	        	fw.write(answer);
    	        	}
    	        	catch (Exception e) {
    	                System.out.println("写文件出错");
    	                e.printStackTrace();
    	            }
            	if(answer.equals(true_answer)) count = count + 1;
            	break;
            }
        }
    }
    /*******问题分类********/
    public static String query_classifier(String query){
    	if(query.matches(".*谁.*")||query.matches(".*的人叫.*")||query.matches(".*的人是.*")||query.matches(".*名字.*")||query.matches(".*哪位.*")||query.matches(".*什么人.*")){
    		return "Name";
    	}
    	if(query.matches(".*首都.*")){
    		return "Capital";
    	}
    	if(query.matches(".*什么颜色.*")||query.matches(".*颜色是什么.*")||query.matches(".*哪种颜色.*")){
    		return "Color";
    	}
    	if(query.matches(".*哪里.*")||query.matches(".*哪儿.*")||query.matches(".*什么地方.*")){
    		return "Location";//不准
    	} 	    	
    	if(query.matches(".*下一句.*")){
    		return "Next_Sentence";
    	}
    	if(query.matches(".*朝代.*")){
    		return "Dynasty";
    	}
    	if(query.matches(".*哪年.*")||query.matches(".*哪一年.*")){
    		return "Year_Number";//不准
    	}
    	if(query.matches(".*多少年.*")||query.matches(".*几年.*")){
    		return "Year_Count";//不准
    	}
    	if(query.matches(".*几月几号.*")||query.matches(".*几月几日.*")){
    		return "Month_Day";//不准
    	}    
    	if(query.matches(".*哪个月.*")||query.matches(".*几月.*")){
    		return "Month";
    	}    	
    	if(query.matches(".*几号.*")||query.matches(".*几日.*")||query.matches(".*哪天.*")||query.matches(".*哪一天.*")){
    		return "Day";//不准
    	}
    	if(query.matches(".*什么时间.*")||query.matches(".*什么时候.*")||query.matches(".*何时.*")||query.matches(".*多少时间.*")||query.matches(".*多长时间.*")||query.matches(".*时间是.*")){
    		return "Time";//不准
    	} 	
    	if(query.matches(".*哪国.*")||query.matches(".*哪.*个国家.*")||query.matches(".*哪个.*国家.*")||query.matches(".*国籍.*")){
    		return "Country";
    	}
    	if(query.matches(".*哪个省.*")||query.matches(".*省份.*")){//省份有bug
    		return "Province";
    	}
    	if(query.matches(".*哪.*个.*城市.*")||query.matches(".*哪个市.*")||query.matches(".*哪.*座城市.*")){
    		return "City";
    	}
    	if(query.matches(".*几.*")||query.matches(".*多少.*")){
    		return "Count";//不准
    	}    	
    	return "Unknown";
    }
    public static void main(String argv[]){
    	/*
    	String rootPath = "G:\\java_workspace\\WebDataMining\\src\\z\\";
    	for(int i=1;i<=23;i++){
    		if(i==16) continue;
    		
    		String ii = i + "";
    		String filePath = rootPath + "z_full_questions_recommend_sentences_part" + ii + ".txt";
    		System.out.println(filePath);
    		readTxtFile(filePath);
    	}//测试数据
    	*/
    	//训练数据
    	
    	
    	String filePath = "G:\\java_workspace\\WebDataMining\\src\\final\\z_online_questions_recommend_sentences_part15.txt";
    	//String filePath = "G:\\java_workspace\\WebDataMining\\src\\question_recommend_sentences_with_question_tmp.txt";

    	
    	readTxtFile(filePath);
        //System.out.println(count);
    }
}
 