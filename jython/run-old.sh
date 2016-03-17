#/bin/bash
# edit the classpath to to the location of your ABAGAIL jar file
#
export CLASSPATH=../ABAGAIL.jar:$CLASSPATH

#mkdir -p data/plot data/logs data/image
mkdir -p data/logs data/image

mkdir -p data/TravelingSalesProblem
mkdir -p data/Knapsack
mkdir -p data/4Peaks

#mkdir -p data/plot/TravelingSalesProblem
#mkdir -p data/plot/Knapsack
#mkdir -p data/plot/4Peaks

mkdir -p data/image/TravelingSalesProblem
mkdir -p data/image/Knapsack
mkdir -p data/image/4Peaks

python prepTSP.py

## four peaks
#echo "four peaks"
#jython fourpeaks.py
#
## count ones
#echo "count ones"
#jython countones.py
#
## continuous peaks
#echo "continuous peaks"
# jython continuouspeaks.py
#
# knapsack
#echo "Running knapsack"
#jython knapsack.py -i 2333

clear
# travelingSalesMan
echo "Traveling Salesman"
echo "Each algorithm varying iterations"

#jython travelingsalesman.py -g --gaIters 1000
#jython travelingsalesman.py -g --gaIters 2000
#jython travelingsalesman.py -g --gaIters 3000
#jython travelingsalesman.py -g --gaIters 4000
#jython travelingsalesman.py -g --gaIters 5000
#jython travelingsalesman.py -g --gaIters 6000
#jython travelingsalesman.py -g --gaIters 7000
#jython travelingsalesman.py -g --gaIters 8000
#jython travelingsalesman.py -g --gaIters 9000
#jython travelingsalesman.py -g --gaIters 10000

jython travelingsalesman.py -s -n 1 -i 20000
jython travelingsalesman.py -s -n 2 -i 20000
jython travelingsalesman.py -s -n 3 -i 20000
	
jython travelingsalesman.py -s -n 1 -i 40000
jython travelingsalesman.py -s -n 2 -i 40000
jython travelingsalesman.py -s -n 3 -i 40000
	
jython travelingsalesman.py -s -n 1 -i 60000
jython travelingsalesman.py -s -n 2 -i 60000
jython travelingsalesman.py -s -n 3 -i 60000

jython travelingsalesman.py -s -n 1 -i 80000
jython travelingsalesman.py -s -n 2 -i 80000
jython travelingsalesman.py -s -n 3 -i 80000
	
jython travelingsalesman.py -s -n 1 -i 100000
jython travelingsalesman.py -s -n 2 -i 100000
jython travelingsalesman.py -s -n 3 -i 100000

jython travelingsalesman.py -s -n 1 -i 120000
jython travelingsalesman.py -s -n 2 -i 120000
jython travelingsalesman.py -s -n 3 -i 120000
	
#jython travelingsalesman.py -s -i 1000 
#jython travelingsalesman.py -m
