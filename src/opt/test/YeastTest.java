package opt.test;

import func.nn.backprop.BackPropagationNetwork;
import func.nn.backprop.BackPropagationNetworkFactory;
import opt.OptimizationAlgorithm;
import opt.RandomizedHillClimbing;
import opt.SimulatedAnnealing;
import opt.example.NeuralNetworkOptimizationProblem;
import opt.ga.StandardGeneticAlgorithm;
import shared.DataSet;
import shared.ErrorMeasure;
import shared.Instance;
import shared.SumOfSquaresError;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.text.DecimalFormat;
import java.util.Scanner;

/**
 * Implementation of randomized hill climbing, simulated annealing, and genetic algorithm to
 * find optimal weights to a neural network that is classifying abalone as having either fewer 
 * or more than 15 rings. 
 *
 * @author Hannah Lau
 * @version 1.0
 */
public class YeastTest {
    private static ProgressBar pBar = new ProgressBar();
    private static Instance[] instances = initializeInstances();
    private static Instance[] testInstances = initializeInstancesTest();

    private static int inputLayer = 8, hiddenLayer = 9, outputLayer = 10, trainingIterations = 1000;
    private static BackPropagationNetworkFactory factory = new BackPropagationNetworkFactory();
    
    private static ErrorMeasure measure = new SumOfSquaresError();

    private static DataSet set = new DataSet(instances);

    private static BackPropagationNetwork networks[] = new BackPropagationNetwork[3];
    private static NeuralNetworkOptimizationProblem[] nnop = new NeuralNetworkOptimizationProblem[3];

    private static OptimizationAlgorithm[] oa = new OptimizationAlgorithm[3];
    private static String[] oaNames = {"RHC", "SA", "GA"};
    private static String results = "";

    private static DecimalFormat df = new DecimalFormat("0.000");

    public static void main(String[] args) {
        if(args.length>0) {
            System.out.println("ARGSS!");
        }
        for(int i = 0; i < oa.length; i++) {
            networks[i] = factory.createClassificationNetwork(
                new int[] {inputLayer, hiddenLayer, outputLayer});
            nnop[i] = new NeuralNetworkOptimizationProblem(set, networks[i], measure);
        }

        oa[0] = new RandomizedHillClimbing(nnop[0]);
        oa[1] = new SimulatedAnnealing(1E11, .95, nnop[1]);
        oa[2] = new StandardGeneticAlgorithm(400, 200, 20, nnop[2]);

        for(int i = 0; i < oa.length; i++) {
            double start = System.nanoTime(), end, trainingTime, testingTime, correct = 0, incorrect = 0;
            train(oa[i], networks[i], oaNames[i]); //trainer.train();
            end = System.nanoTime();
            trainingTime = end - start;
            trainingTime /= Math.pow(10,9);

            Instance optimalInstance = oa[i].getOptimal();
            networks[i].setWeights(optimalInstance.getData());
            //System.out.println(optimalInstance.toString());
            double predicted = 0, actual;
            start = System.nanoTime();
            for(int j = 0; j < instances.length; j++) {
                networks[i].setInputValues(instances[j].getData());
                networks[i].run();
                //System.out.println("Label: " + instances[j].getLabel());
                String[] labels = instances[j].getLabel().toString().replaceAll(" ","").split(",");
                int k = 0;
                double temp = 0;
                for(String label : labels) {
                    if(Double.parseDouble(label) > temp) {
                        temp = Double.parseDouble(label);
                        predicted = k;
                    }
                    k++;
                }
                //System.out.println("Actual outputs: " + networks[i].getOutputValues().toString());
                actual = (networks[i].getDiscreteOutputValue());
                //System.out.println("Predicted: " + predicted + " Actual: " + actual);
                double trash = Math.abs(predicted - actual) < 0.1 ? correct++ : incorrect++;
            }
            end = System.nanoTime();
            testingTime = end - start;
            testingTime /= Math.pow(10,9);

            results +=  "\nResults for " + oaNames[i] + ": \nCorrectly classified " + correct + " instances." +
                        "\nIncorrectly classified " + incorrect + " instances.\nPercent correctly classified: "
                        + df.format(correct/(correct+incorrect)*100) + "%\nTraining time: " + df.format(trainingTime)
                        + " seconds\nTesting time: " + df.format(testingTime) + " seconds\n";
        }
        System.out.println(results);
        results = "";
        for(int i = 0; i < oa.length; i++) {
            double predicted = 0, actual;
            double start = System.nanoTime(), end, trainingTime, testingTime, correct = 0, incorrect = 0;
            start = System.nanoTime();
            for(int j = 0; j < testInstances.length; j++) {
                networks[i].setInputValues(testInstances[j].getData());
                networks[i].run();
                //System.out.println("Label: " + testInstances[j].getLabel());
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
                //System.out.println("Actual outputs: " + networks[i].getOutputValues().toString());
                actual = (networks[i].getDiscreteOutputValue());
                //System.out.println("Predicted: " + predicted + " Actual: " + actual);
                double trash = Math.abs(predicted - actual) < 0.1 ? correct++ : incorrect++;
            }
            end = System.nanoTime();
            testingTime = end - start;
            testingTime /= Math.pow(10,9);

            results +=  "\nResults for " + oaNames[i] + ": \nCorrectly classified " + correct + " testInstances." +
                    "\nIncorrectly classified " + incorrect + " testInstances.\nPercent correctly classified: "
                    + df.format(correct/(correct+incorrect)*100) + "%\nTesting time: " + df.format(testingTime) + " seconds\n";

        }
        System.out.println(results);
    }

    private static void train(OptimizationAlgorithm oa, BackPropagationNetwork network, String oaName) {
        //System.out.println("\nError results for " + oaName + "\n---------------------------");
        System.out.println(oaName + " training progress:");
        pBar.update(0,trainingIterations);
        for(int i = 0; i < trainingIterations; i++) {

            oa.train();

            double error = 0;
            for(int j = 0; j < instances.length; j++) {
                network.setInputValues(instances[j].getData());
                network.run();

                Instance output = instances[j].getLabel(), example = new Instance(network.getOutputValues());
                example.setLabel(new Instance(network.getOutputValues()));
                //System.out.println("Instance output: " + output.getContinuous(0) + " Example output: " + example.getLabel().getContinuous(0));
                error += measure.value(output, example);
            }
            pBar.update(i,trainingIterations);
            //System.out.println(df.format(error));
        }
        System.out.println(oaName + " training complete!");
    }

    private static Instance[] initializeInstances() {

        //double[][][] attributes = new double[1187][][];
        double[][][] attributes = new double[1187][][];

        try {
            BufferedReader br = new BufferedReader(new FileReader(new File("src/opt/test/yeast-train-normed.txt")));

            for(int i = 0; i < attributes.length; i++) {
                Scanner scan = new Scanner(br.readLine());
                scan.useDelimiter(",");

                attributes[i] = new double[2][];
                attributes[i][0] = new double[8]; // 7 attributes
                attributes[i][1] = new double[10];

                for(int j = 0; j < 8; j++)
                    attributes[i][0][j] = Double.parseDouble(scan.next());

                Double element = (Double.parseDouble(scan.next())) * 10 - 1;
                //System.out.println(element);
                //attributes[i][1][0] = Double.parseDouble(scan.next());
                for(int j = 0; j < 10; j++) {
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
        double[][][] attributes = new double[297][][];

        try {
            BufferedReader br = new BufferedReader(new FileReader(new File("src/opt/test/yeast-test.txt")));

            for(int i = 0; i < attributes.length; i++) {
                Scanner scan = new Scanner(br.readLine());
                scan.useDelimiter(",");

                attributes[i] = new double[2][];
                attributes[i][0] = new double[8]; // 7 attributes
                attributes[i][1] = new double[10];

                for(int j = 0; j < 8; j++)
                    attributes[i][0][j] = Double.parseDouble(scan.next());

                Double element = (Double.parseDouble(scan.next())) * 10 - 1;
                //System.out.println(element);
                //attributes[i][1][0] = Double.parseDouble(scan.next());
                for(int j = 0; j < 10; j++) {
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

}
