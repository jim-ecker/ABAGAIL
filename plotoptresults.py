import sys
import csv
import operator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import glob
columns =['Problem', 'Algorithm', 'N', 'Iterations', 'Run', 'OptimalValue']
path = 'Optimization_Results/' + dt.datetime.today().strftime("%Y-%m-%d")
#path = 'Optimization_Results/file_results.csv'
#files = glob.glob(path + '/*.csv')
dimensions = [10,20]
iters = [10,20,30]
for N in dimensions:
    for iter in iters:
        for x in range(3):
            filePath = path + '/count_ones_'
	    filePath = filePath + 'GA_'
	    filePath = filePath + 'N_'
	    filePath = filePath + str(N) + '_iter_' + str(iter) + '_run_' + str(x) + '.csv'
	    colorSwitch = {
                0: 'r',
                1: 'b',
                2: 'g',
            }                      
	    data = np.genfromtxt(filePath, delimiter=',', skip_footer=3, names=['Result'])
            plt.plot(data['Result'], color=colorSwitch.get(x, 'y'), label='the data')
        plt.show()
#for x in range(len(columns)-1):
#    file = csv.reader(open(filePath),delimiter=',')
#    sortedList = sorted(file, key=operator.itemgetter(x))
#    newPath = path + '/sorted_file.csv'
#    with open(newPath, "wb") as f:
#        fileWriter = csv.writer(f, delimiter=',')
#        for row in sortedList:
#            fileWriter.writerow(row)
#print filePath

