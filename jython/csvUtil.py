import csv
import glob
import sys
import os

def buildFooter(prob, alg, rows, settings):
    rows.append(["Problem", prob])
    rows.append(["Algorithm", alg])
    for label, setting in settings:
        rows.append([label,setting])

def outputFooter(prob, alg, rows, settings) :
    dirName = 'data/' + prob.replace(' ', '')
    fileName = dirName + '/' + prob.replace(' ', '') + '_' + alg + '_'
    for label, setting in settings:
        fileName += label.replace(" ", "_") + '_' + str(setting).replace(" ", "_") + '_'
    fileName += ".csv"
    with open(fileName, 'a') as f:
        fileWriter = csv.writer(f,delimiter=',')
        fileWriter.writerow([])
        for row in rows:
            fileWriter.writerow(row)

def output(prob, alg, path, points, settings) :
    dirName = 'data/' + prob.replace(' ', '')
    fileName = dirName + '/' + prob.replace(' ', '') + '_' + alg + '_'
    for label, setting in settings:
        fileName += label.replace(" ", "_") + '_' + str(setting).replace(" ", "_") + '_'

    fileName += ".csv"
    with open(fileName, 'wb') as f:
        fileWriter = csv.writer(f,delimiter=',')
        for point in path:
            row = []
            row.append(points[point][0])
            row.append(points[point][1])
            fileWriter.writerow(row)
def output2(prob, alg, rows, settings) :
    dirName = 'data/' + prob.replace(' ', '')
    fileName = dirName + '/' + prob.replace(' ', '') + '_' + alg + '_'
    for label, setting in settings:
        fileName += label.replace(" ", "_") + '_' + str(setting).replace(" ", "_") + '_'
    fileName += ".csv"
    with open(fileName, 'wb') as f:
        fileWriter = csv.writer(f,delimiter=',')
        for row in rows:
            fileWriter.writerow(row)

