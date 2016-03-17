# traveling salesman algorithm implementation in jython
# This also prints the index of the points of the shortest route.
# To make a plot of the route, write the points at these indexes 
# to a file and plot them in your favorite tool.

import sys
import getopt
from CityList import CityList
import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.DiscretePermutationDistribution as DiscretePermutationDistribution
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.example.TravelingSalesmanRouteEvaluationFunction as TravelingSalesmanRouteEvaluationFunction
import opt.SwapNeighbor as SwapNeighbor
import opt.ga.SwapMutation as SwapMutation
import opt.example.TravelingSalesmanCrossOver as TravelingSalesmanCrossOver
import opt.example.TravelingSalesmanSortEvaluationFunction as TravelingSalesmanSortEvaluationFunction
import util.ABAGAILArrays as ABAGAILArrays
from csvUtil import outputFooter
from csvUtil import buildFooter
from csvUtil import output
from array import array

"""
Commandline parameter(s):
    none
"""
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
    return settings

def pebkac2(wrong, because):
    return """you\'ve specified a %s greater than your %s""" % (wrong,because)

def pebkac(list, alg, highest, settings):
    if list[max(list)] == highest:
        del list[max(list)]
    text = """\nPlease Check Your %s Params, """ % alg
    text += pebkac2(list[max(list)], list[min(list)])
    del list[max(list)]
    while list[max(list)] != highest:
        text += "\nalso, " + pebkac2(list[max(list)], list[min(list)])
        del list[max(list)]
    text += """\n\nHere\'s your configuration:\n\n"""
    maxn = max(len(label) for label, setting in settings)
    maxd = max(len(str(setting)) for label, setting in settings)
    for label, setting in settings:
        text += '%-*s %s %-*s\n' % (maxn, label, ':', maxd, str(setting))
    print text
    sys.exit(2)

# set N value.  This is the number of points
def main():

    iterations = 200000
    alg = 'all'
    gaPop = 2000
    gaMate = 1500
    gaMutate = 250
    mimicSamples = 500
    mimicToKeep = 100
    saTemp = 1E12
    saCooling = .999
    gaIters = 1000
    mimicIters = 1000
    run = 0
    settings = []

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ahrsgmn:i:", ["gaIters=", "mimicIters=", "gaPop=", "gaMate=", "gaMutate=", "mimicSamples=", "mimicToKeep=", "saTemp=", "saCooling="])
    except:
        print 'travelingsalesman.py -i <iterations>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'travelingsalesman.py -i <iterations>'
            sys.exit(1)
        elif opt == '-i':
            if arg < 1:
                print 'Iterations must be greater than 0'
                sys.exit(2)
            iterations = int(arg)
        elif opt == '-a':
            alg = 'all'
        elif opt == '-r':
            alg = 'RHC'
        elif opt == '-s':
            alg = 'SA'
        elif opt == '-g':
            alg = 'GA'
        elif opt == '-m':
            alg = 'MIMIC'
        elif opt == '--gaPop':
            if arg < 1:
                print 'Population must be greater than 0'
                sys.exit(2)
            gaPop = int(arg)
        elif opt == '--gaMate':
            if arg < 1:
                print 'Mating must be greater than 0'
                sys.exit(2)
            gaMate = int(arg)
        elif opt == '--gaMutate':
            if arg < 1:
                print 'Mutators must be greater than 0'
                sys.exit(2)
            gaMutate = int(arg)
        elif opt == '--mimicSamples':
            if arg < 1:
                print 'MIMIC samples must be greater than 0'
                sys.exit(2)
            mimicSamples = int(arg)
        elif opt == '--mimicToKeep':
            if arg < 1:
                print 'MIMIC to keep must be greater than 0'
                sys.exit(2)
            mimicToKeep = int(arg)
        elif opt == '--saTemp':
            saTemp = float(arg)
        elif opt == '--saCooling':
            saCooling = float(arg)
        elif opt == '-n':
            run = int(arg)
        elif opt == '--gaIters':
            if arg < 1:
                print 'GA Iterations must be greater than 0'
                sys.exit(2)
            gaIters = int(arg)
        elif opt == '--mimicIters':
            if arg < 1:
                print 'MIMIC Iterations must be greater than 0'
                sys.exit(2)
            mimicIters = int(arg)

    vars = {
            'iterations' : iterations,
            'alg' : alg,
            'gaPop' : gaPop,
            'gaMate' : gaMate,
            'gaMutate' : gaMutate,
            'mimicSamples' : mimicSamples,
            'mimicToKeep' : mimicToKeep,
            'saTemp' : saTemp,
            'saCooling' : saCooling,
            'gaIters' : gaIters,
            'mimicIters' : mimicIters,
            'run' : run
            }

    settings = getSettings(alg, settings, vars)
    if gaPop < gaMate or gaPop < gaMutate or gaMate < gaMutate:
        pebkac({gaPop: 'total population',gaMate : 'mating population', gaMutate : 'mutating population'}, alg, 'total population', settings)
    if mimicSamples < mimicToKeep:
        pebkac({mimicSamples: 'mimic samples', mimicToKeep : 'mimic to keep'}, alg, 'mimic samples', settings)
    prob = 'Traveling Sales Problem'
    invDist = {}
    cities = CityList()
    N = len(cities)
    #random = Random()
    points = [[0 for x in xrange(2)] for x in xrange(N)]
    for i in range(0, len(points)):
        coords = cities.getCoords(i)
        points[i][0] = coords[0]
        points[i][1] = coords[1]
    ef = TravelingSalesmanRouteEvaluationFunction(points)
    odd = DiscretePermutationDistribution(N)
    nf = SwapNeighbor()
    mf = SwapMutation()
    cf = TravelingSalesmanCrossOver(ef)
    hcp = GenericHillClimbingProblem(ef, odd, nf)
    gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)
    rows = []


    if alg == 'RHC' or alg == 'all':
        print '\n----------------------------------'
        print 'Using Random Hill Climbing'
        for label, setting in settings:
            print label + ":" + str(setting)
        rhc = RandomizedHillClimbing(hcp)
        fit = FixedIterationTrainer(rhc, iterations)
        fit.train()
        path = []
        for x in range(0,N):
            path.append(rhc.getOptimal().getDiscrete(x))
        output(prob, 'RHC', path, points, settings)
        rows = []
        row = []
        row.append("Inverse of Distance")
        row.append(ef.value(rhc.getOptimal()))
        rows.append(row)
        invDist['RHC'] = ef.value(rhc.getOptimal())
        buildFooter(prob, 'RHC', rows, settings)
        outputFooter(prob, 'RHC', rows, settings)


    if alg == 'SA' or alg == 'all':
        print 'Using Simulated Annealing'
        for label, setting in settings:
            print label + ":" + str(setting)
        sa = SimulatedAnnealing(saTemp, saCooling, hcp)
        fit = FixedIterationTrainer(sa, iterations)
        fit.train()
        path = []
        for x in range(0,N):
            path.append(sa.getOptimal().getDiscrete(x))
        output(prob, 'SA', path, points, settings)
        rows = []
        row = []
        row.append("Inverse of Distance")
        row.append(ef.value(sa.getOptimal()))
        rows.append(row)
        invDist['SA'] = ef.value(sa.getOptimal())
        buildFooter(prob, 'SA', rows, settings)
        outputFooter(prob, 'SA', rows, settings)

    if alg == 'GA' or alg == 'all':
        print '\n----------------------------------'
        print 'Using Genetic Algorithm'
        for label, setting in settings:
            print label + ":" + str(setting)
        ga = StandardGeneticAlgorithm(gaPop, gaMate, gaMutate, gap)
        fit = FixedIterationTrainer(ga, gaIters)
        fit.train()
        path = []
        for x in range(0,N):
            path.append(ga.getOptimal().getDiscrete(x))
        output(prob, 'GA', path, points, settings)
        rows = []
        row = []
        row.append("Inverse of Distance")
        row.append(ef.value(ga.getOptimal()))
        rows.append(row)
        invDist['GA'] = ef.value(ga.getOptimal())
        buildFooter(prob, 'GA', rows, settings)
        outputFooter(prob, 'GA', rows, settings)

    if alg == 'MIMIC' or alg == 'all':
        print '\n----------------------------------'
        print 'Using MIMIC'
        for label, setting in settings:
            print label + ":" + str(setting)
        # for mimic we use a sort encoding
        ef = TravelingSalesmanSortEvaluationFunction(points);
        fill = [N] * N
        ranges = array('i', fill)
        odd = DiscreteUniformDistribution(ranges);
        df = DiscreteDependencyTree(.1, ranges);
        pop = GenericProbabilisticOptimizationProblem(ef, odd, df);
        mimic = MIMIC(mimicSamples, mimicToKeep, pop)
        fit = FixedIterationTrainer(mimic, mimicIters)
        fit.train()
        path = []
        optimal = mimic.getOptimal()
        fill = [0] * optimal.size()
        ddata = array('d', fill)
        for i in range(0,len(ddata)):
            ddata[i] = optimal.getContinuous(i)
        order = ABAGAILArrays.indices(optimal.size())
        ABAGAILArrays.quicksort(ddata, order)
        output(prob, 'MIMIC', order, points, settings)
        rows = []
        row = []
        row.append("Inverse of Distance")
        row.append(ef.value(mimic.getOptimal()))
        rows.append(row)
        invDist['MIMIC'] = ef.value(mimic.getOptimal())
        buildFooter(prob, 'MIMIC', rows, settings)
        outputFooter(prob, 'MIMIC', rows, settings)


    maxn = max(len(key) for key in invDist)
    maxd = max(len(str(invDist[key])) for key in invDist)
    print "Results"
    for result in invDist:
        print "%-*s %s %-*s" % (len('Best Alg') + 2, result, ':', maxd, invDist[result])
    if alg == 'all':
        print "%-*s %s %-*s" % (len('Best Alg') + 2, 'Best Alg', ':', maxd, max(invDist.iterkeys(), key=(lambda key: invDist[key])))
    print '----------------------------------'

if __name__ == "__main__":
    main()