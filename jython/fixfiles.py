import sys
import os
import csv
import glob

probs=['TravelingSalesProblem', 'Knapsack', '4Peaks']
for prob in probs:
    files = glob.glob('data/' + prob + '/*.csv')
    for file in files:
        oldname = file
        file = file.replace(" ", "_")
        file = file.replace("__", "_")
	os.rename(oldname, file)
    
