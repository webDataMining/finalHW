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

public class Answer_Retrieval1 {
	static Segment segment = HanLP.newSegment().enableAllNamedEntityRecognize(true);
	/**************颜色********************/
	public int Answer_color(String query, String ans_type, ArrayList<String> cand, ArrayList<String> keywords, String true_answer){
    	int find = 0;
    	String answer = "";
    	WordJudge wj = new WordJudge();
    	for(String sentence: cand){
    		List<Term> termList = segment.seg(sentence);
    		for(Term t:termList){
    			String word = t.word;
    			if(wj.isColor(word)){
    				if(query.indexOf(word)>=0) continue;
    				find = 1;
    				answer = word;
    				break;
    			}
    		}
    		if(find == 1) break;
    	}
    	if(find == 1){
    		System.out.println(answer);
	    	
    		if(answer.equals(true_answer)){
    			return 1;
    		}
    	}
    	return 0;
	}
	/*************省份********************/
	public int Answer_province(String query, String ans_type, ArrayList<String> cand, ArrayList<String> keywords, String true_answer){
		String [] province_vector = {"北京","河北","天津","重庆","上海","黑龙江","辽宁","吉林","内蒙古","河北","山东","山西","河南","甘肃","宁夏","陕西","新疆","青海","西藏","四川","云南","广西",
				"江苏","安徽","浙江","福建","广东","江西","湖南","湖北","台湾","贵州","海南","香港","澳门"};
    	int find = 0;
    	String answer = "";
    	int cand_count = cand.size();
    	for(int tmp0 = 0; tmp0<cand_count; tmp0 = tmp0 + 1){
    		String sentence = cand.get(tmp0);
    		String key = keywords.get(tmp0);
    		for(String prov : province_vector){
    			if(key.indexOf(prov)>=0){
    				if(query.indexOf(key)<0){
    				find = 1;
    				answer = prov;
    				break;
    				}
    			}
    		}
        	if(find == 1){
        		System.out.println(answer);
        		if(answer.equals(true_answer)){
        			return 1;
        		}
        	}   		
    		List<Term> termList = segment.seg(sentence);
    		for(Term t:termList){
    			String word = t.word;
        		for(String prov : province_vector){
        			if(word.indexOf(prov)>=0){
        				if(query.indexOf(word)<0){
        				find = 1;
        				answer = prov;
        				break;
        				}
        			}
        		}
        		if(find==1) break;
    		}
    		if(find == 1) break;
    	}
    	if(find == 1){
    		System.out.println(answer);
    		if(answer.equals(true_answer)){
    			return 1;
    		}
    	}    	
		return 0;
	}
	/**************市*********************/
	public int Answer_city(String query, String ans_type, ArrayList<String> cand, ArrayList<String> keywords, String true_answer){
    	int find = 0;
    	String answer = "";
    	WordJudge wj = new WordJudge();
    	for(String sentence: cand){
    		List<Term> termList = segment.seg(sentence);
    		for(Term t:termList){
    			String word = t.word;
    			if(wj.isCity(word)){
    				if(query.indexOf(word)>=0) continue;
    				find = 1;
    				answer = word.substring(0, word.length()-1);
    				break;
    			}
    		}
    		if(find == 1) break;
    	}
    	if(find==0){
        	for(String sentence: cand){
        		List<Term> termList = segment.seg(sentence);
        		for(Term t:termList){
        			String word = t.word;
        			if(t.nature.toString()=="ns"||t.nature.toString()=="nsf"){
        				if(query.indexOf(word)>=0) continue;
        				find = 1;
        				answer = word;
        				break;
        			}
        		}
        		if(find == 1) break;
        	}
    	}
    	if(find == 1){
    		System.out.println(answer);
    		if(answer.equals(true_answer)){
    			return 1;
    		}
    	}
    	return 0;
	}
	/*************朝代******************/
	public int Answer_dynasty(String query, String ans_type, ArrayList<String> cand, ArrayList<String> keywords, String true_answer){
		String [] dynasty_vector = {"夏","商","周","秦","西楚","汉","东汉","西汉","魏","蜀","吴","晋","刘宋","南齐","南梁","南陈","北魏","东魏","北齐","隋","唐","北宋",
				"南宋","宋","五代","十国","南北朝","辽","西夏","金","元","明","清"};
		
    	int find = 0;
    	String answer = "";
    	int cand_count = cand.size();
    	for(int tmp0 = 0; tmp0<cand_count; tmp0 = tmp0 + 1){
    		String sentence = cand.get(tmp0);
    		String key = keywords.get(tmp0);
    		for(String prov : dynasty_vector){
    			if(key.indexOf(prov)>=0){
    				if(query.indexOf(key)<0){
    				find = 1;
    				answer = prov;
    				break;
    				}
    			}
    		}
        	if(find == 1){
        		System.out.println(answer);
        		if(answer.equals(true_answer)){
        			return 1;
        		}
        	}   		
    		List<Term> termList = segment.seg(sentence);
    		for(Term t:termList){
    			String word = t.word;
        		for(String prov : dynasty_vector){
        			if(word.indexOf(prov)>=0){
        				if(query.indexOf(word)<0){
        				find = 1;
        				answer = prov;
        				break;
        				}
        			}
        		}
        		if(find==1) break;
    		}
    		if(find == 1) break;
    	}
    	if(find == 1){
    		System.out.println(answer);
    		if(answer.equals(true_answer)){
    			return 1;
    		}
    	}    	
		return 0;
	}
	
}
