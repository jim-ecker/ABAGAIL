package func.test;

import shared.ConvergenceTrainer;
import shared.DataSet;
import shared.Instance;
import shared.SumOfSquaresError;
import func.nn.backprop.BackPropagationNetwork;
import func.nn.backprop.BackPropagationNetworkFactory;
import func.nn.backprop.BatchBackPropagationTrainer;
import func.nn.backprop.RPROPUpdateRule;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.Scanner;

/**
 * A simple classification test
 * @author Andrew Guillory gtg008g@mail.gatech.edu
 * @version 1.0
 */
public class NNClassificationYeast {

    /**
     * Tests out the perceptron with the classic xor test
     * @param args ignored
     */
    private static Instance[] instances = initializeInstances();
    public static void main(String[] args) {
        BackPropagationNetworkFactory factory = 
            new BackPropagationNetworkFactory();
        //double[][][] data = {
        //    { { 1, 1 }, { .1, .9 } },
        //    { { 0, 1 }, { 0, 1 } },
        //    { { 0, 0 }, { .9, .1 } }
        //};
        //Instance[] patterns = new Instance[data.length];
        //for (int i = 0; i < patterns.length; i++) {
        //    patterns[i] = new Instance(data[i][0]);
        //    patterns[i].setLabel(new Instance(data[i][1]));
        //}
        BackPropagationNetwork network = factory.createClassificationNetwork(
           new int[] { 8, 9, 1 });
        DataSet set = new DataSet(instances);
        ConvergenceTrainer trainer = new ConvergenceTrainer(
               new BatchBackPropagationTrainer(set, network,
                   new SumOfSquaresError(), new RPROPUpdateRule()));
        trainer.train();
        System.out.println("Convergence in " 
            + trainer.getIterations() + " iterations");
        for (int i = 0; i < instances.length; i++) {
            network.setInputValues(instances[i].getData());
            network.run();
            System.out.println("~~");
            System.out.println(instances[i].getLabel());
            System.out.println(network.getOutputValues());
        }
    }
    private static Instance[] initializeInstances() {

        double[][][] attributes = new double[1187][][];

        try {
            BufferedReader br = new BufferedReader(new FileReader(new File("src/opt/test/yeast-train-normed.txt")));

            for(int i = 0; i < attributes.length; i++) {
                Scanner scan = new Scanner(br.readLine());
                scan.useDelimiter(",");

                attributes[i] = new double[2][];
                attributes[i][0] = new double[8]; // 7 attributes
                attributes[i][1] = new double[1];

                for(int j = 0; j < 8; j++)
                    attributes[i][0][j] = Double.parseDouble(scan.next());

                attributes[i][1][0] = Double.parseDouble(scan.next());
            }
        }
        catch(Exception e) {
            e.printStackTrace();
        }

        Instance[] instances = new Instance[attributes.length];

        for(int i = 0; i < instances.length; i++) {
            instances[i] = new Instance(attributes[i][0]);
            // classifications range from 0 to 30; split into 0 - 14 and 15 - 30
            instances[i].setLabel(new Instance(attributes[i][1][0]));
        }

        return instances;
    }
}
