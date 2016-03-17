__author__ = 'Jimmy'

from Runner import Runner

class FourPeaksRunner(Runner):
    def __init__(self):
        super(FourPeaksRunner, self).__init__()
        self.argmap = {
            'iterations'        : '-i',

            'alg':  {

                'all'       : '-a',
                'RHC'       :'-r',
                'SA'        : '-s',
                'GA'        : '-g',
                'MIMIC'     : '-m'

            },

            'gaPop'             : '--gaPop',
            'gaMate'            : '--gaMate',
            'gaMutate'          : '--gaMutate',
            'mimicSamples'      : '--mimicSamples',
            'mimicToKeep'       : '--mimicToKeep',
            'saTemp'            : '--saTemp',
            'saCooling'         : '--saCooling',
            'gaIters'           : '--gaIters',
            'mimicIters'        : '--mimicIters',
            'run'               : '-n'
        }
        self.setProblems('4Peaks')
        self.setArgMap({'N':'-n'})
        self.setArgMap({'tempDenom' : '-d'})
        self.setArgMap({'T' : '-t'})
        self.setFiles({self.problems[0]: 'fourpeaks.py'})
        self.setBaseCommands(self.problems[0], self.files[self.problems[0]])
        self.setAlgs(['RHC','SA','GA','MIMIC'])
        params = dict(RHC=[dict(iter='-i')], SA=[dict(param1='--saTemp', param2='--saCooling', iter='-i')],
                      GA=[dict(iter='--gaIters', param1='--gaPop', param2='--gaMate', param3='--gaMutate')],
                      MIMIC=[dict(param1='--mimicSamples', param2='--mimicToKeep', iter='--mimicIters')])
        self.setParams(params)

    def four(self):
        self.sendCommand(self.parseArgs(self.package, self.baseCommands[self.problems[0]]))
