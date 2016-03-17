package opt.test;

import java.io.*;
import java.util.*;

/**
 * Created by Jimmy on 3/6/16.
 */
public class NormalizeData {

    public static void main(String[] args) {
        String filename = "src/opt/test/yeast-test.txt";
        try {
            BufferedReader br = new BufferedReader(new FileReader(new File(filename)));
            PrintWriter out = new PrintWriter("src/opt/test/yeast-test-2.txt");
            for(int i = 0; i < 297; i++) {
                StringBuilder output = new StringBuilder();
                Scanner scan = new Scanner(br.readLine());
                scan.useDelimiter(",");
                for(int j = 0; j < 8; j++) {
                    output.append(scan.next());
                    output.append(",");
                }
                double normalized = Double.parseDouble(scan.next())/10.0;
                output.append(normalized);
                out.println(output.toString());
            }
            out.close();
            br.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
