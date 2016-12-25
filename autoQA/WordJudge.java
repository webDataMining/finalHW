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
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
public class WordJudge {
	
	public boolean isColor(String word){
		if(word.indexOf("绿色")>0||word.indexOf("红色")>0||word.indexOf("橙色")>0||word.indexOf("黄色")>0||word.indexOf("红色")>0||word.indexOf("青色")>0||word.indexOf("蓝色")>0||word.indexOf("紫色")>0
				||word.indexOf("灰色")>0||word.indexOf("白色")>0||word.indexOf("黑色")>0){
			return true;
		}
		return false;
	}
	public boolean isCity(String word){
		if(word.indexOf("市")>=0){
			return true;
		}
		return false;
	}
	public int countjudge(String query){
		if(query.matches(".*第几.*")) return 1;
		else if(query.matches("是多少")||query.matches("有多少")||query.matches("为多少")) return 2;
		else if(query.matches("几个")) return 3;
		else if(query.matches("多少")) return 4;
		else if(query.matches("几")) return 5;
		return 6;
	}
	public boolean nyrjudge(String query){
		if(query=="年"||query=="月"||query=="日") return true;
		return false;
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
	}

}
