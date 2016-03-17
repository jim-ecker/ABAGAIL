import os
import sys
import time
from Runner import Runner
from TSPRunner import TSPRunner
from KnapsackRunner import KnapsackRunner
from FourPeaksRunner import FourPeaksRunner
from NNRunner import NNRunner
import getopt
import math

def usage():
    print """run.py
        --baseline  wipes all files and runs baseline performance scripts"""
def main():
    tsp = TSPRunner()
    knap = KnapsackRunner()
    four = FourPeaksRunner()
    nn = NNRunner()
    runner = Runner()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["baseline"])
    except:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(1)
        elif opt == '--baseline':
            tsp.baseLine()

    for i in range(1,11):
        for j in range(1,11):
            algs = ('alg', 'all')
            iter = ('iterations', j * 1000)
            runs = ('run', j)
            temp = ('saTemp' , i * 10**(11))
            cooling = ('saCooling', i * 100)
            pop = ('gaPop', j * 10)
            mate = ('gaMate', j * 5)
            mute = ('gaMutate', j * 2)
            samples = ('mimicSamples', 200)
            tokeep = ('mimicToKeep', 20)
            package = [iter, runs, algs, temp, cooling, pop, mate, mute, samples, tokeep]
            runner.packageBuilder(package)
            #tsp.setPackage(runner.package)
            knap.setPackage(runner.package)
            #four.setPackage(runner.package)
            #tsp.tsp()
            knap.knap()
            #four.four()

#    #for i in range(1,11):
#        for j in range(1, 11):
#            iter = ('iterations', i * 1000)
#            temp = ('saTemp' , 10**(i+11))
#            cooling = ('saCooling', 0.999)
#            pop = ('gaPop', i * 100)
#            mate = ('gaMate', j * (i * 10))
#            mute = ('gaMutate', int((i * 10)) * 0.5)
#            n = ('run', j)
#            package = [iter, n, temp, cooling, pop, mate, mute]
#            runner.packageBuilder(package)
#            nn.setPackage(runner.package)
#            nn.nn()

if __name__ == "__main__":
    main()
