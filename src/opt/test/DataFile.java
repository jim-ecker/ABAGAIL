package opt.test;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * Created by Jimmy on 3/12/16.
 */
public class DataFile {
    private int lineCount;
    private String fileName;
    private BufferedReader tempBr;
    private BufferedReader br;

    public DataFile() {
        this.lineCount = 0;
        this.fileName = "";
    }

    public DataFile(String fileName) {
        this.fileName = fileName;
        try {
            this.open();
        }
        catch (Exception e) { e.printStackTrace(); }
        this.lineCount = this.countLines();
    }

    private int countLines() {
        this.openTemp();
        int lines = 0;
        try {
            while (tempBr.readLine() != null) lines++;
        }
        catch (Exception e) { e.printStackTrace(); }
        this.closeTemp();
        return lines;
    }

    public void open() {
        try {
            this.br = new BufferedReader(new FileReader(new File("./" + this.fileName)));
        }
        catch (Exception e) { e.printStackTrace(); }
    }

    public void openTemp() {
        try {
            this.tempBr = new BufferedReader(new FileReader(new File("./" + this.fileName)));
        }
        catch (Exception e) { e.printStackTrace(); }
    }

    public void close() {
        try {
            this.br.close();
        }
        catch (Exception e) { e.printStackTrace(); }
    }

    public void closeTemp() {
        try {
            this.tempBr.close();
        }
        catch (Exception e) { e.printStackTrace(); }
    }

    public int getLineCount() {
        return this.lineCount;
    }

    public String getFileName() {
        return this.fileName;
    }

    public String nextLine() {
        //this.open();
        String next = "";
        try {
            next = br.readLine();
        }
        catch(Exception e) { e.printStackTrace(); }
        //this.close();
        return next;
    }

    public ArrayList<String> nextLine(String delim) {
        //this.open();
        ArrayList<String> nextLine = new ArrayList<String>();
        try {
            Scanner scan = new Scanner(br.readLine());
            scan.useDelimiter(delim);
            while(scan.hasNext()) {
                nextLine.add(scan.next());
            }
        }
        catch (Exception e) { e.printStackTrace(); }
        //this.close();
        return nextLine;
    }
}
