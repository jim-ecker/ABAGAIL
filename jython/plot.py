import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import glob
import itertools
import getopt
import os

from CityList import CityList

def fix(alg, prob, measure):
    erase = 0
    fds = getFDs(searchFiles('GA', prob), prob)
    for fd in fds:
       for row in fd:
           if len(row) > 2:
               os.remove(fd['Name'])

def optimusPrime(alg, prob, measure):
    fds = getFDs(searchFiles(alg, prob), prob)
    for fd in fds:
        if measure in fd:
            if prob != 'NN':
                optimal = max(fd[measure] for fd in fds)
            else:
                optimal = min(fd[measure] for fd in fds)
            if fd[measure] == optimal:
                return { optimal : fd['Name'] }

def getFDLength(file):
    return getDataLength(file) - getDataLength('data/TravelingSalesProblem/TSP_cities_DB.csv')
def getDataLength(file):
    i = 0
    f = csv.reader(open(file), delimiter=",")
    for row in f:
        i = i + 1
    return i

def sortLists(x, y):
    none = True
    while none:
        none = False
        for i in range(0, len(x) - 1):
            if float(x[i]) > float(x[i+1]):
                none = True
                tempx = x[i]
                tempy = y[i]
                x[i] = x[i+1]
                y[i] = y[i+1]
                x[i+1] = tempx
                y[i+1] = tempy
    sorted = {'x': x, 'y': y}
    return sorted

def getFDs(files, prob):
    fds = []
    for file in files:
        if prob == 'TravelingSalesProblem':
            n = getFDLength(file)
        else:
            n = 0
        fds.append(buildFD(file, n))
    return fds

def buildFD(file, num):
    f = csv.reader(open(file), delimiter=',')
    footerDict = {}
    slice = []
    for row in f:
        if row != []:
            slice.append(row)
    rows = slice[-num:]
    for row in rows:
        footerDict[row[0]] = row[1]
        footerDict['Name'] = file
    return footerDict

def searchFiles(query, prob):
    caught = []
    files = glob.glob('data/' + prob + '/*.csv')
    for file in files:
        alg = find_between(file, '_', '_')
        if alg == query:
            caught.append(file)
    return caught

def saveGraph(plt, x, y, alg, prob):
    algs = {'RHC' : 'Random Hill Climbing', 'SA' : 'Simulated Annealing' , 'GA' : 'Genetic Algorithm', 'MIMIC' : "MIMIC"}
    fileName = 'data/image/' + prob + "/" + alg + "_performance_" + prob + "_" + y + "_over_" + x
    if prob == "TravelingSalesProblem":
        titleProblem = "Traveling Sales Problem"
    if prob == "Knapsack":
        titleProblem = "Knapsack"
    if prob == "4Peaks":
        titleProblem = "Four Peaks"
    if prob == "NN":
        titleProblem = "Neural Network"
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(algs[alg] + " performance on " + titleProblem + "\n" + y + " varying " + x + ' over time', y=1.03)
    plt.show()
    plt.savefig(fileName)

def grabValues(file, n):
    data = []
    f = csv.reader(open(file))
    for i in range(n):
        for row in itertools.islice(f, n, None):
            data.append(row)
    return data

def getAverages(x, y):
    newXs = []
    newYs = []
    curr = 0
    discrete = [list(j) for i,j in itertools.groupby(x)]
    groupedYs = []
    theseYs = []
    for i in range(0, len(y)):
        if curr == 0 and i == 0:
            theseYs = []
            newXs.append(x[curr])
        if x[curr] not in newXs and curr != 0:
            theseYs = []
            groupedYs.append(theseYs)
            newXs.append(x[curr])
        for j in range(curr, len(y)):
            if x[j] == x[curr]:
                theseYs.append(y[j])
            else:
                curr = j
                break
    groupedYs.append(theseYs)
    for i in range(len(groupedYs)):
        sumYs = 0
        for j in range(len(groupedYs[i])):
            sumYs += float(groupedYs[i][j])
        newYs.append(sumYs/float(len(groupedYs[i])))
    return [newXs, newYs]

def getXY(files, prob, x):
    xData = []
    yData = []
    fds = getFDs(files, prob)
    for fd in fds:
        yData.append(fd[getMeasure(prob)])
        xData.append(fd[x])
    return [xData, yData]
def whittle(x, files, y, prob, realx):
    cities = CityList()
    whittled = []
    for file in files:
        if prob != 'TravelingSalesProblem':
            n = 0
        else:
            n = getDataLength(file)
        fileDescriptor = buildFD(file, n)
        for key in fileDescriptor:
            if type(x) == type(dict()):
                for xkey in x:
                    if key == xkey:
                        if int(fileDescriptor[key]) == (x[xkey]):
                            whittled.append(fileDescriptor['Name'])
            elif key == x:
                whittled.append(fileDescriptor['Name'])
    return files

def nplot(x,y,plt, run):
    colormap = plt.cm.gist_ncar
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, run)])
    plt.plot(x, y, marker='o', label='the data')
    return plt

def plot(x,y):
    colormap = plt.cm.gist_ncar
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, 1)])
    plt.gcf().subplots_adjust(top=0.88, right=.87)
    plt.plot(x, y, marker='o', label='the data')
    return plt

def performance(alg, x, prob, y):
    files = searchFiles(alg, prob)
    whittled = whittle(x, files, y, prob, x)
    xy = getXY(whittled, prob, x)
    sorted = sortLists(xy[0], xy[1])
    avgs = getAverages(sorted['x'], sorted['y'])
    return avgs

def nperformance(alg, x, prob, y):
    files = searchFiles(alg, prob)
    fds = getFDs(files, prob)
    for i in range(1,int(countRuns(fds)) + 1):
        whittled = whittle({'Run': i}, files, y, prob, x)
        whittled = whittle(x, whittled, y, prob, 'Iterations')
        xy = getXY(files, prob, x)
        sorted = sortLists(xy[0], xy[1])
        avgs = getAverages(sorted['x'], sorted['y'])
        #colormap = plt.cm.gist_ncar
        #plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, 20)])
        plt.plot(avgs[0], avgs[1])
    saveGraph(plt, x, y, alg, prob)


def countRuns(fds):
    return max(fd['Run'] for fd in fds)


def map(prob):
    algs = {'RHC' : 'Random Hill Climbing', 'SA' : 'Simulated Annealing' , 'GA' : 'Genetic', 'MIMIC' : "MIMIC"}
    cities = CityList()
    for alg in algs:
        files = searchFiles(alg, 'TravelingSalesProblem')
        if len(files) > 0:
            for file in files:
                if alg == 'cities':
                    continue
                mapThisOne(file)

def mapThisOne(file, prob):
    cities = CityList()
    data = np.genfromtxt(file, delimiter=',', skip_footer = 0, names=['x', 'y'])
    plt.gcf().subplots_adjust(bottom=0.310)
    plt.plot(data['x'], data['y'], marker='o', color='r', label='the data')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    if prob != 'TravelingSalesProblem':
        footerDict = buildFD(file, 0)
    else:
        footerDict = buildFD(file, getFDLength(file))
    text = prob + " optimized by " + footerDict['Algorithm']
    if footerDict['Algorithm'] == 'RHC':
        if 'Mating' in footerDict:
            del footerDict['Mating']
        if 'Mutation' in footerDict:
            del footerDict['Mutation']
        if 'Population' in footerDict:
            if 'Population' in footerDict:
                del footerDict['Population']
        if 'To Keep' in footerDict:
            del footerDict['To Keep']
        if 'Samples' in footerDict:
            del footerDict['Samples']
        if 'Cooling' in footerDict:
            del footerDict['Cooling']
        if 'Temperature' in footerDict:
            del footerDict['Temperature']
    if footerDict['Algorithm'] == 'SA':
        if 'Mating' in footerDict:
            del footerDict['Mating']
        if 'Mutation' in footerDict:
            del footerDict['Mutation']
        if 'Population' in footerDict:
            del footerDict['Population']
        if 'To Keep' in footerDict:
            del footerDict['To Keep']
        if 'Samples' in footerDict:
            del footerDict['Samples']
    if footerDict['Algorithm'] == 'GA':
        if 'To Keep' in footerDict:
            del footerDict['To Keep']
        if 'Samples' in footerDict:
            del footerDict['Samples']
        if 'Cooling' in footerDict:
            del footerDict['Cooling']
        if 'Temperature' in footerDict:
            del footerDict['Temperature']
    if footerDict['Algorithm'] == 'MIMIC':
        if 'Mating' in footerDict:
            del footerDict['Mating']
        if 'Mutation' in footerDict:
            del footerDict['Mutation']
        if 'Population' in footerDict:
            del footerDict['Population']
        if 'Cooling' in footerDict:
            del footerDict['Cooling']
        if 'Temperature' in footerDict:
            del footerDict['Temperature']
    plt.text(-115,15, text, horizontalalignment='center', verticalalignment='center')
    print footerDict
    labeltext = ''
    valuetext = ''
    for key in footerDict:
        if key == 'Name':
            continue
        labeltext += '\n' + key
        valuetext += '\n' + footerDict[key]
    plt.title('Traveling Salesman Problem Through Cities \nin Which Ludacris Claims to Have Female Aquaintances')
    plt.text(-160,5, labeltext, horizontalalignment='left')
    plt.text(-140,5, valuetext, horizontalalignment='left')
    imageName = file.replace('csv', 'png')
    fig = plt.gcf()

    fig.set_size_inches(10, 8)
    fig.savefig('test2png.png', dpi=100)
    plt.savefig(imageName)
    plt.show()
    plt.clf()

def printFD(file, prob):
    fd = buildFD(file, getDataLength(file))

    print fd
    for key in fd:
        print str(key) + " " + str(fd[key])

def find_between(s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getMeasure(prob):
    if prob == 'TravelingSalesProblem':
        return 'Inverse of Distance'
    elif prob == 'Knapsack' or prob == '4Peaks':
        return 'Evaluation Function Value'
    else:
        return 'RMSE'

def main():
    prob = ''
    mode = ''
    file = ''
    params = {}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:m:f:", ['alg=', 'x=', 'y='])
    except:
        print 'plot.py -p <problem> -m <mode>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-p':
            prob = arg
        if opt == '-m':
            mode = arg
        if opt == '-f':
            mode = 'file'
            file = arg
        if opt == '--alg':
            params['alg'] = arg
        if opt == '--x':
            params['x'] = arg
        if opt == '--y':
            params['y'] = arg

    if mode == 'map':
        map(prob)

    if mode == 'performance':
        if len(params) <= 0:
           sys.exit(2)
        sorted = performance(params['alg'], params['x'], prob, getMeasure(prob))
        saveGraph(plot(sorted[0], sorted[1]), params['x'], getMeasure(prob), params['alg'], prob)

    if mode == 'nperformance':
        if len(params) <= 0:
            sys.exit(2)
        nperformance(params['alg'], params['x'], prob, getMeasure(prob))

    if mode == 'file':
        n = getDataLength(file)
        fd = buildFD(file, 0)
        prob = fd['Problem']
        alg = fd['Algorithm']
        measure = getMeasure(prob)
        sorted = performance(alg, params['x'], prob, measure)
        saveGraph(plot(sorted['x'], sorted['y']), params['x'], measure, alg, prob)

    if mode == 'optimal':
        optimums = {}
        if params['alg'] == "ALL":
            algs = ["RHC", "SA", "GA", "MIMIC"]
            if prob == 'NN':
                algs = ["RHC", "SA", "GA"]
        else:
            algs = [params['alg']]
        for alg in algs:
            optimum = optimusPrime(alg, prob, getMeasure(prob))
            print optimum
            for key in optimum:
                print key
                optimums[key] = optimum[key]
        if prob == 'TravelingSalesProblem':
            mapThisOne(optimums[max(opt for opt in optimums)], prob)
        elif prob == 'Knapsack' or prob == '4Peaks':
            printFD(optimums[max(opt for opt in optimums)], prob)
        else:
            printFD(optimums[min(opt for opt in optimums)], prob)


    if mode == 'fix':
        if params['alg'] == "ALL":
            algs = ["RHC", "SA", "GA", "MIMIC"]
        else:
            algs = [params['alg']]
        for alg in algs:
            fix(alg, prob, getMeasure(prob))


if __name__ == "__main__":
    main()