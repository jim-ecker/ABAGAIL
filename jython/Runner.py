__author__ = 'Jimmy'
import time
import os
import sys



class Runner(object):
    def __init__(self):
        self.executionCommand = 'jython'
        self.package = {}
        self.commands = []
        self.counter = range(1,110)
        self.files= {}
        self.algs = []
        self.params = {}
        self.problems = []
        self.plotter = "plot.py"
        self.argmap = {}
        self.baseCommands = {}
        for problem in self.problems:
            command = self.executionCommand + ' ' + self.files[problem]
            self.setBaseCommands(problem, command)
        self.setProblems([file for file in self.files])

    def setPackage(self, arg):
        for key in arg:
            self.package[key] = arg[key]

    def resetPackage(self):
        self.package = {}

    def packageBuilder(self, pair):
        for var, val in pair:
            arg = {}
            arg[var] = val
            self.setPackage(arg)

    def setExecutionCommand(self, command):
        self.executionCommand = command

    def setBaseCommands(self, name, command):
        self.baseCommands[name] = self.executionCommand + " " + command

    def setArgMap(self, args):
        for arg in args:
            self.argmap[arg] = args[arg]

    def resetArgMap(self):
        self.argmap = {}

    def setFiles(self, files):
        for key in files:
            self.files[key] = files[key]

    def setAlgs(self, algs):
        for key in algs:
            self.algs.append(key)

    def setParams(self, params):
        for key in params:
            self.params[key] = params[key]

    def setProblems(self, problems):
        for problem in problems:
            self.problems.append(problem)

    def graphCommandBuilder(self, prob, mode, alg, x):
        return 'python ' + self.plotter + " -p " + prob + ' -m ' + mode + ' --alg ' + alg + " --x " + x

    def graphBuilder(self, mode, x):
        graphCommands = []
        for problem in self.problems:
            for alg in self.algs:
                graphCommands.append(self.graphCommandBuilder(problem, mode, alg, x))
        return graphCommands

    def sendCommand(self, command):
        if 'python' not in command:
            os.system("rm run.sh")
            os.system("cp run-cache.sh run.sh")
            os.system("echo " + command + " >> run.sh")
            os.system("source run.sh")
        else:
            os.system(command)

    def parseArgs(self, args, command):
        for arg in args:
            if type(self.argmap[arg]) is dict:
                command += ' ' + self.argmap[arg][args[arg]]
            else:
                if arg in self.argmap:
                    command += ' ' + self.argmap[arg]
                    command += ' ' + str(args[arg])
                else:
                    command += arg
        print command
        return command

    def baseLine(self):
        os.system('rm -rf data/')
        self.commands.append('mkdir -p data/logs data/image')
        self.commands.append('mkdir -p data/TravelingSalesProblem')
        self.commands.append('mkdir -p data/Knapsack')
        self.commands.append('mkdir -p data/4Peaks')
        self.commands.append('mkdir -p data/image/TravelingSalesProblem')
        self.commands.append('mkdir -p data/image/Knapsack')
        self.commands.append('mkdir -p data/image/4Peaks')
        for file in self.files:
            for alg in self.algs:
                for param in self.params[alg]:
                    for pos, i in enumerate(self.counter):
                        if i % 10 == 0:
                            command = 'jython '
                            command += file + ' '
                            command += self.algs[alg] + ' '
                            num = i * 100
                            command += self.params[alg][0]['iter'] + ' '
                            command += str(num)
                            self.commands.append(command)
        os.system("rm run.sh")
        time.sleep(1)
        os.system("rm -rf data/")
        time.sleep(1)
        os.system("cp run-cache.sh run.sh")
        time.sleep(1)
        for command in self.commands:
            os.system("echo " + command + " >> run.sh")
        #time.sleep(1)
        #for command in self.graphBuilder("performance", "Iterations"):
        #    os.system("echo " + command + " >> run.sh")
        os.system("source run.sh")