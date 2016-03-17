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

    settings.append(('N' , vars['N']))
    settings.append(('Temp Denominator' , vars['tempDenom']))
    settings.append(('T' , vars['T']))
    return settings

"""
Commandline parameter(s):
   none
"""
def main():
    N=200
    tempDenom = 5
    T=N/tempDenom
    fill = [2] * N
    ranges = array('i', fill)
    iterations = 2000
    gaIters = 1000
    mimicIters = 1000
    gaPop = 200
    gaMate = 100
    gaMutate = 10
    mimicSamples = 200
    mimicToKeep = 20
    saTemp = 1E11
    saCooling = .95
    alg = 'all'
    run = 0
    settings = []

    try:
       opts, args = getopt.getopt(sys.argv[1:], "ahn:rsgN:m:t:i:", ["gaIters=", "mimicIters=","gaPop=", "gaMate=", "gaMutate=", "mimicSamples=", "mimicToKeep=", "saTemp=", "saCooling="])
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
          N = int(arg)
       elif opt == '-t':
           T = float(arg)
       elif opt == '-d':
          tempDenom = int(arg)
       elif opt == '-r':
           alg = 'RHC'
       elif opt == '-a':
           alg = 'all'
       elif opt == '-s':
           alg = 'SA'
       elif opt == '-g':
           alg = 'GA'
       elif opt == '-m':
           alg = 'MIMIC'
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
       elif opt == '-n':
           run = int(arg)


    vars = {
        'N':N,
        'tempDenom':tempDenom,
        'T':T,
        'fill':fill,
        'ranges':ranges,
        'iterations' :iterations,
        'gaIters':gaIters,
        'mimicIters':mimicIters,
        'gaPop' :gaPop,
        'gaMate' :gaMate,
        'gaMutate' :gaMutate,
        'mimicSamples' : mimicSamples,
        'mimicToKeep' : mimicToKeep,
        'saTemp' : saTemp,
        'saCooling' : saCooling,
        'alg' : alg,
        'run' : run
    }

    settings = getSettings(alg, settings, vars)

    T=N/tempDenom
    fill = [2] * N
    ranges = array('i', fill)

    ef = FourPeaksEvaluationFunction(T)
    odd = DiscreteUniformDistribution(ranges)
    nf = DiscreteChangeOneNeighbor(ranges)
    mf = DiscreteChangeOneMutation(ranges)
    cf = SingleCrossOver()
    df = DiscreteDependencyTree(.1, ranges)
    hcp = GenericHillClimbingProblem(ef, odd, nf)
    gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
    pop = GenericProbabilisticOptimizationProblem(ef, odd, df)

    if alg == 'RHC' or alg == 'all':
        rhc = RandomizedHillClimbing(hcp)
        fit = FixedIterationTrainer(rhc, iterations)
        fit.train()
        rows = []
        row = []
        row.append("Evaluation Function Value")
        row.append(ef.value(rhc.getOptimal()))
        rows.append(row)
        print "RHC: " + str(ef.value(rhc.getOptimal()))
        output2('4Peaks', 'RHC', rows, settings)
        rows = []
        buildFooter("4Peaks", "RHC", rows, settings),
        outputFooter("4Peaks", "RHC", rows,   settings)

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
        output2('4Peaks', 'SA', rows, settings)
        rows = []
        buildFooter("4Peaks", "SA", rows, settings)
        outputFooter("4Peaks", "SA", rows, settings)

    if alg == 'GA' or alg == 'all':
        ga = StandardGeneticAlgorithm(gaPop, gaMate, gaMutate, gap)
        fit = FixedIterationTrainer(ga, gaIters)
        fit.train()
        print "GA: " + str(ef.value(ga.getOptimal()))
        rows = []
        row = []
        row.append("Evaluation Function Value")
        row.append(ef.value(ga.getOptimal()))
        rows.append(row)
        output2('4Peaks', 'GA', rows, settings)
        rows = []
        buildFooter("4Peaks", "GA", rows, settings)
        outputFooter("4Peaks", "GA", rows , settings)

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
        output2('4Peaks', 'MIMIC', rows, settings)
        rows = []
        buildFooter("4Peaks", "GA", rows, settings)
        outputFooter("4Peaks", "MIMIC", rows, settings)

if __name__ == "__main__":
    main()