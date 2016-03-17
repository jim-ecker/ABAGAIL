import sys
import os
import time


import java.io.FileReader as FileReader
import java.io.File as File
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.Distribution as Distribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.EvaluationFunction as EvaluationFunction
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.HillClimbingProblem as HillClimbingProblem
import opt.NeighborFunction as NeighborFunction
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.example.FourPeaksEvaluationFunction as FourPeaksEvaluationFunction
import opt.ga.CrossoverFunction as CrossoverFunction
import opt.ga.SingleCrossOver as SingleCrossOver
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.GeneticAlgorithmProblem as GeneticAlgorithmProblem
import opt.ga.MutationFunction as MutationFunction
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.ga.UniformCrossOver as UniformCrossOver
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import opt.prob.ProbabilisticOptimizationProblem as ProbabilisticOptimizationProblem
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.example.KnapsackEvaluationFunction as KnapsackEvaluationFunction
from array import array
import getopt
from csvUtil import outputFooter
from csvUtil import buildFooter
from csvUtil import output2

def getSettings(alg, settings, vars):
    if alg == 'RHC':
        settings = [('Iterations', vars['iterations'])]
    elif alg == 'SA':
        settings = [('Temperature', vars['saTemp']), ('Cooling', vars['saCooling']), ("Iterations", vars['iterations'])]
    elif alg == 'GA':
        settings = [('Population', vars['gaPop']), ('Mating', vars['gaMate']), ('Mutation', vars['gaMutate']), ('Iterations', vars['gaIters'])]
    elif alg == 'MIMIC':
        settings = [('Samples', vars['mimicSamples']), ('To Keep', vars['mimicToKeep']), ('Iterations', vars['mimicIters'])]
    else:
        settings = [('Temperature', vars['saTemp']), ('Cooling', vars['saCooling']), ("Iterations", vars['iterations']), ('Population', vars['gaPop']), ('Mating', vars['gaMate']), ('Mutation', vars['gaMutate']), ('Samples', vars['mimicSamples']), ('To Keep', vars['mimicToKeep'])]
    if vars['run'] > 0:
        settings.append(('Run', vars['run']))
    check = []
    for label, setting in settings:
        check.append(label.lower())

    settings.append(('Num Items' , vars['NUM_ITEMS']))
    settings.append(('Copies_Each' , vars['COPIES_EACH']))
    settings.append(('Max Weight' , vars['MAX_WEIGHT']))
    settings.append(('Max Volume' , vars['MAX_VOLUME']))
    return settings

"""
Commandline parameter(s):
    none
"""
def main():

    # The number of items
    NUM_ITEMS = 40
    # The number of copies each
    COPIES_EACH = 4
    # The maximum weight for a single element
    MAX_WEIGHT = 50
    # The maximum volume for a single element
    MAX_VOLUME = 50

    iterations = 20000
    gaIters = 1000
    mimicIters = 1000
    gaPop = 200
    gaMate = 150
    gaMutate = 25
    mimicSamples = 200
    mimicToKeep = 100
    saTemp = 100
    saCooling = .95
    alg = 'all'
    run = 0
    settings = []

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ahrsgmn:N:c:w:v:i:", ["gaIters=", "mimicIters=","gaPop=", "gaMate=", "gaMutate=", "mimicSamples=", "mimicToKeep=", "saTemp=", "saCooling="])
    except:
        print 'knapsack.py -i <iterations> -n <NUM_ITEMS> -c <COPIES_EACH> -w <MAX_WEIGHT> -v <MAX_VOLUME>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'knapsack.py -i <iterations> -n <NUM_ITEMS> -c <COPIES_EACH> -w <MAX_WEIGHT> -v <MAX_VOLUME>'
            sys.exit(1)
        elif opt == '-i':
            iterations = int(arg)
        elif opt == '-N':
            NUM_ITEMS = int(arg)
        elif opt == '-c':
            COPIES_EACH = int(arg)
        elif opt == '-w':
            MAX_WEIGHT = int(arg)
        elif opt == '-v':
            MAX_VOLUME = int(arg)
        elif opt == '-n':
            run = int(arg)
        elif opt == '-r':
            alg = 'RHC'
        elif opt == '-s':
            alg = 'SA'
        elif opt == '-g':
            alg = 'GA'
        elif opt == '-m':
            alg = 'MIMIC'
        elif opt == '-a':
            alg = 'all'
        elif opt == '--gaPop':
            gaPop = int(arg)
        elif opt == '--gaMate':
            gaMate = int(arg)
        elif opt == '--gaMutate':
            gaMutate = int(arg)
        elif opt == '--mimicSamples':
            mimicSamples = int(arg)
        elif opt == '--mimicToKeep':
            mimicToKeep = int(arg)
        elif opt == '--saTemp':
            saTemp = float(arg)
        elif opt == '--saCooling':
            saCooling = float(arg)
        elif opt == '--gaIters':
            gaIters = int(arg)
        elif opt == '--mimicIters':
            mimicIters = int(arg)
    vars ={
    'NUM_ITEMS' : NUM_ITEMS,
    'COPIES_EACH' : COPIES_EACH,
    'MAX_WEIGHT' : MAX_WEIGHT,
    'MAX_VOLUME' : MAX_VOLUME,
    'iterations' : iterations,
    'gaIters' : gaIters,
    'mimicIters' : mimicIters,
    'gaPop' : gaPop,
    'gaMate' : gaMate,
    'gaMutate' : gaMutate,
    'mimicSamples' : mimicSamples,
    'mimicToKeep' : mimicToKeep,
    'saTemp' : saTemp,
    'saCooling' : saCooling,
    'alg' : alg,
    'run' : run
    }

    settings = getSettings(alg, settings, vars)
    # Random number generator */
    random = Random()

    # The volume of the knapsack
    KNAPSACK_VOLUME = MAX_VOLUME * NUM_ITEMS * COPIES_EACH * .4

    # create copies
    fill = [COPIES_EACH] * NUM_ITEMS
    copies = array('i', fill)

    # create weights and volumes
    fill = [0] * NUM_ITEMS
    weights = array('d', fill)
    volumes = array('d', fill)
    for i in range(0, NUM_ITEMS):
        weights[i] = random.nextDouble() * MAX_WEIGHT
        volumes[i] = random.nextDouble() * MAX_VOLUME


    # create range
    fill = [COPIES_EACH + 1] * NUM_ITEMS
    ranges = array('i', fill)

    ef = KnapsackEvaluationFunction(weights, volumes, KNAPSACK_VOLUME, copies)
    odd = DiscreteUniformDistribution(ranges)
    nf = DiscreteChangeOneNeighbor(ranges)
    mf = DiscreteChangeOneMutation(ranges)
    cf = UniformCrossOver()
    df = DiscreteDependencyTree(.1, ranges)
    hcp = GenericHillClimbingProblem(ef, odd, nf)
    gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df)

    if alg == 'RHC' or alg == 'all':
        rhc = RandomizedHillClimbing(hcp)
        fit = FixedIterationTrainer(rhc, iterations)
        fit.train()
        print "RHC: " + str(ef.value(rhc.getOptimal()))
        rows = []
        row = []
        row.append("Evaluation Function Value")
        row.append(str(ef.value(rhc.getOptimal())))
        rows.append(row)
        output2('Knapsack', 'RHC', rows, settings)
        rows = []
        buildFooter("Knapsack", "RHC", rows, settings)
        outputFooter("Knapsack", "RHC", rows , settings)
    if alg == 'SA' or alg == 'all':
        sa = SimulatedAnnealing(saTemp, saCooling, hcp)
        fit = FixedIterationTrainer(sa, iterations)
        fit.train()
        rows = []
        row = []
        row.append("Evaluation Function Value")
        row.append(ef.value(sa.getOptimal()))
        rows.append(row)
        print "SA: " + str(ef.value(sa.getOptimal()))
        output2('Knapsack', 'SA', rows, settings)
        rows = []
        buildFooter("Knapsack", "SA", rows, settings)
        outputFooter("Knapsack", "SA", rows, settings)
    if alg == 'GA' or alg == 'all':
        ga = StandardGeneticAlgorithm(gaPop, gaMate, gaMutate, gap)
        fit = FixedIterationTrainer(ga, gaIters)
        fit.train()
        rows = []
        row = []
        row.append("Evaluation Function Value")
        row.append(ef.value(ga.getOptimal()))
        rows.append(row)
        print "GA: " + str(ef.value(ga.getOptimal()))
        output2('Knapsack', 'GA', rows, settings)
        buildFooter("Knapsack", "GA", rows, settings)
        outputFooter("Knapsack", "GA", rows , settings)
    if alg == 'MIMIC' or alg == 'all':
        mimic = MIMIC(mimicSamples, mimicToKeep, pop)
        fit = FixedIterationTrainer(mimic, mimicIters)
        fit.train()
        print "MIMIC: " + str(ef.value(mimic.getOptimal()))
        rows = []
        row = []
        row.append("Evaluation Function Value")
        row.append(ef.value(mimic.getOptimal()))
        rows.append(row)
        output2('Knapsack', 'MIMIC', rows, settings)
        rows = []
        buildFooter("Knapsack", "MIMIC", rows, settings)
        outputFooter("Knapsack", "MIMIC", rows , settings)

if __name__ == "__main__":
    main()
