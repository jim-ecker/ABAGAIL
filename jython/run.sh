#/bin/bash
# edit the classpath to to the location of your ABAGAIL jar file
#
export CLASSPATH=../ABAGAIL.jar:$CLASSPATH
mkdir -p data/logs data/image
mkdir -p data/TravelingSalesProblem
mkdir -p data/Knapsack
mkdir -p data/4Peaks
mkdir -p data/image/TravelingSalesProblem
mkdir -p data/image/Knapsack
mkdir -p data/image/4Peaks
jython knapsack.py --saCooling 1000 --gaMate 50 -a --gaMutate 20 --saTemp 1000000000000 --gaPop 100 -i 10000 --mimicSamples 200 -n 10 --mimicToKeep 20
