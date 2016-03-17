__author__ = 'Jimmy'

from Runner import Runner

class NNRunner(Runner):
    def __init__(self):
        super(NNRunner, self).__init__()
        self.argmap = {
            'iterations'        : 'iterations=',
            'data'              : '',
            'algs'              : 'algs=',
            'gaPop'             : 'gaPop=',
            'gaMate'            : 'gaMate=',
            'gaMutate'          : 'gaMutate=',
            'saTemp'            : 'saTemp=',
            'saCooling'         : 'saCooling=',
            'gaIters'           : 'gaIters=',
            'run'               : 'run='
        }
        self.setProblems('NN')
        self.setExecutionCommand("java -cp ABAGAIL.jar")
        self.setFiles({self.problems[0]: 'opt.test.NNTest wine'})
        self.setBaseCommands(self.problems[0], self.files[self.problems[0]])
        self.setAlgs(['RHC', 'SA', 'GA'])
        params = dict(RHC=[dict(iter='-i')], SA=[dict(param1='--saTemp', param2='--saCooling', iter='-i')],
                      GA=[dict(iter='--gaIters', param1='--gaPop', param2='--gaMate', param3='--gaMutate')],
                      MIMIC=[dict(param1='--mimicSamples', param2='--mimicToKeep', iter='--mimicIters')])
        self.setParams(params)

    def parseArgs(self, args, command):
        for arg in args:
            if type(self.argmap[arg]) is dict:
                command += ' ' + self.argmap[arg][args[arg]]
            else:
                if arg in self.argmap:
                    command += ' ' + self.argmap[arg]
                    command += str(args[arg])
                else:
                    command += arg
        print "Generated Command: "+ command
        return command


    def nn(self):
        self.sendCommand(self.parseArgs(self.package, self.baseCommands[self.problems[0]]))
