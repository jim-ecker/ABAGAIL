package opt.test;

import dist.*;
import opt.*;
import opt.example.*;
import opt.ga.*;
import shared.*;
import func.nn.backprop.*;
import util.linalg.DenseVector;

import java.awt.image.AreaAveragingScaleFilter;
import java.util.*;
import java.io.*;
import java.text.*;

/**
 * Implementation of randomized hill climbing, simulated annealing, and genetic algorithm to
 * find optimal weights to a neural network that is classifying abalone as having either fewer 
 * or more than 15 rings. 
 *
 * @author Hannah Lau
 * @version 1.0
 */
public class NNTest {
    private static ProgressBar pBar = new ProgressBar();

    private static int convergence;
    private static int inputLayer = 13, hiddenLayer = 8, outputLayer = 3;
    private static int trainingIterations = 1000;
    private static BackPropagationNetworkFactory factory = new BackPropagationNetworkFactory();
    
    private static ErrorMeasure measure = new SumOfSquaresError();


    private static BackPropagationNetwork networks[] = new BackPropagationNetwork[3];
    private static NeuralNetworkOptimizationProblem[] nnop = new NeuralNetworkOptimizationProblem[3];

    private static ArrayList<OptimizationAlgorithm> oa = new ArrayList<>();

    private static StringBuilder rhcSb = new StringBuilder();
    private static StringBuilder saSb = new StringBuilder();
    private static StringBuilder gaSb = new StringBuilder();

    private static String[] oaNames = {"RHC", "SA", "GA"};
    private static String results = "";

    private static DecimalFormat df = new DecimalFormat("0.000");

    public static void main(String[] args) {
        double saTemp = 1E11;
        double saCooling = .95;
        double RMSE = 0;
        int gaPop = 200;
        int gaMate = 100;
        int gaMutate = 50;
        String data = "";
        int run = 0;
        if(args.length == 1) {
            data = args[0];
            if(!checkData(data))
                System.exit(1);
        }
        else if (args.length > 1) {
            data = args[0];
            if(!checkData(data))
                System.exit(1);
            try {
                Queue<String> cmdArgs = new LinkedList<>();
                for(int i = 1; i < args.length; i++) {
                    cmdArgs.add(args[i]);
                }
                Iterator<String> qIter = cmdArgs.iterator();
                while(qIter.hasNext()){
                    String[] command = qIter.next().split("=");
                    if(command[0].equals("saTemp")){
                        try {
                            saTemp = Double.parseDouble(command[1]);
                        }
                        catch (Exception e) { e.printStackTrace(); }
                    }
                    if(command[0].equals("saCooling")){
                        try {
                            saTemp = Double.parseDouble(command[1]);
                        }
                        catch (Exception e) { e.printStackTrace(); }
                    }
                    if(command[0].equals("gaPop")){
                        try {
                            saTemp = Integer.parseInt(command[1]);
                        }
                        catch (Exception e) { e.printStackTrace(); }
                    }
                    if(command[0].equals("gaMate")){
                        try {
                            saTemp = Integer.parseInt(command[1]);
                        }
                        catch (Exception e) { e.printStackTrace(); }
                    }
                    if(command[0].equals("gaMutate")){
                        try {
                            saTemp = Integer.parseInt(command[1]);
                        }
                        catch (Exception e) { e.printStackTrace(); }
                    }
                    if(command[0].equals("algs")){
                        try {
                            String[] algsToUse = command[1].split("-");
                            oaNames = new String[algsToUse.length];
                            nnop = new NeuralNetworkOptimizationProblem[oaNames.length];
                            int i = 0;
                            for(String alg : algsToUse) {
                                oaNames[i] = alg.toUpperCase();
                                i++;
                            }
                        }
                        catch (Exception e) { e.printStackTrace(); }
                    }
                    if(command[0].equals("iterations")){
                        trainingIterations = Integer.parseInt(command[1]);
                        if(trainingIterations < 0) {
                            System.out.println("trainingIterations must be greater than 0\n\nUsage: java -cp ABAGAIL.jar opt.test.NNTest req: <testType> opt: <trainingIteration>\n\nSupported test types: \n\twine\n\tyeast\n\ntrainingIterations must be gt 0\n");
                            System.exit(1);
                        }
                    }
                    if(command[0].equals("run")){
                        run = Integer.parseInt(command[1]);
                    }
                }
            }
            catch (Exception e) { e.printStackTrace(); }
        }
        else {
            System.out.println("Incorrect arguments\n\nUsage: java -cp ABAGAIL.jar opt.test.NNTest req: <testType> opt: <trainingIteration>\n\nSupported test types:\n\twine\n\tyeast\n\ntrainingIterations must be gt 0\n");
            System.exit(1);
        }

        String trainingFileName = data.toLowerCase() + "-train.txt";
        String testingFileName = data.toLowerCase() + "-test.txt";
        DataFile trainingDf = new DataFile(trainingFileName);
        DataFile testingDf = new DataFile(testingFileName);

        Instance[] trainInstances = initializeInstances(trainingDf, inputLayer, outputLayer);
        Instance[] testInstances = initializeInstances(testingDf, inputLayer, outputLayer);

        DataSet set = new DataSet(trainInstances);
        networks = new BackPropagationNetwork[oaNames.length];
        for(int i = 0; i < oaNames.length; i++) {
            networks[i] = factory.createClassificationNetwork(
                new int[] {inputLayer, hiddenLayer, outputLayer});
            nnop[i] = new NeuralNetworkOptimizationProblem(set, networks[i], measure);
        }
        int i = 0;
        for(String alg : oaNames) {
           if(alg.toUpperCase().equals("RHC")) {
               try {
                   oa.add(new RandomizedHillClimbing(nnop[i]));
               }
               catch (Exception e) { e.printStackTrace(); }
            }
            if(alg.toUpperCase().equals("SA")) {
                try {
                    oa.add(new SimulatedAnnealing(saTemp, saCooling, nnop[i]));
                }
                catch (Exception e) { e.printStackTrace(); }
            }
            if(alg.toUpperCase().equals("GA")){
                try {
                    oa.add(new StandardGeneticAlgorithm(gaPop, gaMate, gaMutate, nnop[i]));
                }
                catch (Exception e) { e.printStackTrace(); }
            }
            i++;
        }


        for(i = 0; i < oa.size(); i++) {
            results = "";
            double start = System.nanoTime(), end, trainingTime, testingTime, correct = 0, incorrect = 0;
            convergence = 0;
            train(oa.get(i), networks[i], oaNames[i]); //trainer.train();
            end = System.nanoTime();
            trainingTime = end - start;
            trainingTime /= Math.pow(10,9);

            Instance optimalInstance = oa.get(i).getOptimal();
            networks[i].setWeights(optimalInstance.getData());
            double predicted = 0, actual;
            start = System.nanoTime();
            for(int j = 0; j < trainInstances.length; j++) {
                networks[i].setInputValues(trainInstances[j].getData());
                networks[i].run();
                String[] labels = trainInstances[j].getLabel().toString().replaceAll(" ","").split(",");
                int k = 0;
                double temp = 0;
                for(String label : labels) {
                    if(Double.parseDouble(label) > temp) {
                        temp = Double.parseDouble(label);
                        predicted = k;
                    }
                    k++;
                }
                actual = (networks[i].getDiscreteOutputValue());
                double trash = Math.abs(predicted - actual) < 0.1 ? correct++ : incorrect++;
            }
            end = System.nanoTime();
            testingTime = end - start;
            testingTime /= Math.pow(10,9);
            RMSE = Math.pow((correct - incorrect), 2)/trainingIterations;
            results +=  "\n---------------------------------------------------------";
            results += "\n" + "Results for " + oaNames[i] + ": ";
            results +=  "\n---------------------------------------------------------";
            results +=  "\nTraining Data Results: ";
            results +=  "\nCorrectly classified " + correct + " instances." +
                        "\nIncorrectly classified " + incorrect + " instances.\nPercent correctly classified: "
                        + df.format(correct/(correct+incorrect)*100) + "%\nTraining time: " + df.format(trainingTime)
                        + " seconds\nTesting time: " + df.format(testingTime) + " seconds\n";
            if(oaNames[i].equals("RHC")) {
                rhcSb.append(results);
            }
            if(oaNames[i].equals("SA")) {
                saSb.append(results);
            }
            if(oaNames[i].equals("GA")) {
                gaSb.append(results);
            }
            String fileName = "./data/NN/NN_" + oaNames[i] + "_Iterations_" + trainingIterations;
            if(oaNames[i].equals("SA")) {
                fileName += "_Temp_" + saTemp + "_Cooling_" + saCooling;
            }
            if(oaNames[i].equals("GA")) {
                fileName += "_Population_" + gaPop + "_Mating_" + gaMate + "_Mutating_" + gaMutate;
            }
            fileName += "_Train.csv";
            System.out.println("Wrote to " + fileName);
            try {
                FileWriter f = new FileWriter(new File(fileName), false);
                f.append("Iterations");
                f.append(",");
                f.append(String.valueOf(trainingIterations));
                f.append("\n");
                f.append("Correct");
                f.append(",");
                f.append(String.valueOf(correct));
                f.append("\n");
                f.append("Incorrect");
                f.append(",");
                f.append(String.valueOf(incorrect));
                f.append("\n");
                f.append("Percent Correct");
                f.append(",");
                f.append(df.format(correct/(correct+incorrect)*100));
                f.append("\n");
                f.append("RMSE");
                f.append(",");
                f.append(String.valueOf(RMSE));
                f.append("\n");
                f.append("Training Time");
                f.append(",");
                f.append(df.format(testingTime));

                f.flush();
                f.close();

            }
            catch (Exception e) { e.printStackTrace(); }

        }

        for(i = 0; i < oa.size(); i++) {
            results = "";
            double predicted = 0, actual;
            double start = System.nanoTime(), end, trainingTime, testingTime, correct = 0, incorrect = 0;
            start = System.nanoTime();
            for(int j = 0; j < testInstances.length; j++) {
                networks[i].setInputValues(testInstances[j].getData());
                networks[i].run();
                String[] labels = testInstances[j].getLabel().toString().replaceAll(" ","").split(",");
                int k = 0;
                double temp = 0;
                for(String label : labels) {
                    if(Double.parseDouble(label) > temp) {
                        temp = Double.parseDouble(label);
                        predicted = k;
                    }
                    k++;
                }
                actual = (networks[i].getDiscreteOutputValue());
                double trash = Math.abs(predicted - actual) < 0.1 ? correct++ : incorrect++;
            }
            end = System.nanoTime();
            testingTime = end - start;
            testingTime /= Math.pow(10,9);

            results += "\nTest Data Results: ";
            results +=  "\nResults for " + oaNames[i] + ": \nCorrectly classified " + correct + " testInstances." +
                    "\nIncorrectly classified " + incorrect + " testInstances.\nPercent correctly classified: "
                    + df.format(correct/(correct+incorrect)*100) + "%\nTesting time: " + df.format(testingTime) + " seconds\n";
            results +=  "---------------------------------------------------------";

            if(oaNames[i].equals("RHC")) {
                rhcSb.append(results);
            }
            if(oaNames[i].equals("SA")) {
                saSb.append(results);
            }
            if(oaNames[i].equals("GA")) {
                gaSb.append(results);
            }
            String fileName = "./data/NN/NN_" + oaNames[i] + "_Iterations_" + trainingIterations;
            switch (i){
                case 0:
                    break;
                case 1:
                    fileName += "_Temp_" + saTemp + "_Cooling_" + saCooling;
                    break;
                case 2:
                    fileName += "_Population_" + gaPop + "_Mating_" + gaMate + "_Mutating_" + gaMutate;
                    break;
                default:
                    break;
            }
            fileName += "_Test.csv";
            System.out.println(fileName);
            try {
                FileWriter f = new FileWriter(new File(fileName), false);

                f.append("Iterations");
                f.append(",");
                f.append(String.valueOf(trainingIterations));
                f.append("\n");
                f.append("Correct");
                f.append(",");
                f.append(String.valueOf(correct));
                f.append("\n");
                f.append("Incorrect");
                f.append(",");
                f.append(String.valueOf(incorrect));
                f.append("\n");
                f.append("Percent Correct");
                f.append(",");
                f.append(df.format(correct/(correct+incorrect)*100));
                f.append("\n");
                f.append("RMSE");
                f.append(",");
                f.append(String.valueOf(RMSE));
                f.append("\n");
                f.append("Training Time");
                f.append(",");
                f.append(df.format(testingTime));
                f.append("\n");
                f.append("Run");
                f.append(",");
                f.append(String.valueOf(run));

                f.flush();
                f.close();

            }
            catch (Exception e) { e.printStackTrace(); }
        }
        System.out.println(rhcSb.toString());
        System.out.println(saSb.toString());
        System.out.println(gaSb.toString());
        trainingDf.close();
        testingDf.close();
    }

    private static void train(OptimizationAlgorithm oa, BackPropagationNetwork network, String oaName) {
        System.out.println("---------------------------------------------------------\n" + oaName + " training progress:");
        pBar.update(0,trainingIterations);
        for(int i = 0; i < trainingIterations && convergence < 10; i++) {
            double error = 1/oa.train();
            pBar.update(i, trainingIterations);
            System.out.print(" error: " + df.format(error));
            if(error < 0.00009) {
                convergence++;
            }
        }
        System.out.println("\n" + oaName + " training complete\n---------------------------------------------------------");
    }

    private static Instance[] initializeInstances(DataFile df, int numAttributes, int numOutput) {

        double[][][] attributes = new double[df.getLineCount()][][];

        try {
            for(int i = 0; i < attributes.length; i++) {
                ArrayList<String> tokenizedLine = df.nextLine(",");
                Iterator<String> lineIter = tokenizedLine.iterator();

                attributes[i] = new double[2][];
                attributes[i][0] = new double[numAttributes]; // num attributes
                attributes[i][1] = new double[numOutput]; // num outputnodes

                for(int j = 0; j < numAttributes; j++)
                    attributes[i][0][j] = Double.parseDouble(lineIter.next());

                Double element = (Double.parseDouble(lineIter.next())) * 10 - 1;
                for(int j = 0; j < numOutput; j++) {
                    if(j != element) {
                        attributes[i][1][j] = 0;
                    }
                    else
                        attributes[i][1][j] = 1;
                }
            }
        }
        catch(Exception e) {
            e.printStackTrace();
        }

        Instance[] instances = new Instance[attributes.length];

        for(int i = 0; i < instances.length; i++) {
            instances[i] = new Instance(attributes[i][0]);
            instances[i].setLabel(new Instance(attributes[i][1]));
        }
        return instances;
    }

    private static Instance[] initializeInstancesTest() {

        //double[][][] attributes = new double[1187][][];
        double[][][] attributes = new double[36][][];

        try {
            BufferedReader br = new BufferedReader(new FileReader(new File("./wine-test.txt")));

            for(int i = 0; i < attributes.length; i++) {
                Scanner scan = new Scanner(br.readLine());
                scan.useDelimiter(",");

                attributes[i] = new double[2][];
                attributes[i][0] = new double[13]; // 7 attributes
                attributes[i][1] = new double[3];

                for(int j = 0; j < 13; j++)
                    attributes[i][0][j] = Double.parseDouble(scan.next());

                Double element = (Double.parseDouble(scan.next())) * 10 - 1;
                for(int j = 0; j < 3; j++) {
                    if(j != element) {
                        attributes[i][1][j] = 0;
                    }
                    else
                        attributes[i][1][j] = 1;
                }
            }
        }
        catch(Exception e) {
            e.printStackTrace();
        }

        Instance[] instances = new Instance[attributes.length];

        for(int i = 0; i < instances.length; i++) {
            instances[i] = new Instance(attributes[i][0]);
            instances[i].setLabel(new Instance(attributes[i][1]));
        }
        return instances;
    }

    private static boolean checkData(String data) {
        if(data.toLowerCase().equals("yeast")) {
            inputLayer = 8;
            hiddenLayer = 9;
            outputLayer = 10;
        }
        else if (data.toLowerCase().equals("wine")) {

        }
        else{
            System.out.println("Please use supported data type\n\nUsage: java -cp ABAGAIL.jar opt.test.NNTest req: <testType> opt: <trainingIterations>\n\nSupported test types:\n\twine\n\tyeast\n\ntrainingIterations must be gt 0\n");
            return false;
        }
        return true;
    }

}
