#!/usr/bin/env python
import subprocess, re, os,sys 

def chkdir(c):
    if not os.path.isdir(c): subprocess.call(['mkdir', '-p', c])

class condorJob:
    SUBMITCMD = 'condor_submit'
    Executable = 'run_scanVar.exe'
    Universe = 'vanilla'
    GetEnv = 'True'
    requirements = '''(regexp("atint01",Machine)==FALSE)'''

    def __init__(self, odir='outputs/test'):
        self.Arguments = '22 $$([$(Process) - $(Base)]) 0.04 -1 $(outTag)_ $(cutV) $(outDir)/ $(conf)'
        self.Queue = 1

        self.outDir = odir.rstrip('/')
        self.jobTag = 'Job_$(Process)'
        self.Vars = ''
        self.leodir = '/leo/'

    def submit(self, configFile, isTest=False):
        chkdir(self.outDir)
        chkdir(self.outDir+'/leo')
        submit_cmd_path = self.writeScript(self.outDir+'/'+configFile)
        if not isTest: subprocess.call([self.SUBMITCMD, submit_cmd_path])

    def writeScript(self, configFile):
        text = 'Executable = ' + self.Executable + '\n'
        text += 'Universe = ' + self.Universe + '\n'
        text += 'GetEnv = ' + self.GetEnv + '\n'
        text += 'requirements = ' + self.requirements + '\n'
        text += self.Vars + '\n'
        text += 'Error = ' + self.outDir+ self.leodir + self.jobTag + '.err\n'
        text += 'Output = ' + self.outDir+ self.leodir + self.jobTag + '.out\n'
        text += 'Log = ' + self.outDir+ self.leodir + self.jobTag + '.log\n'
        text += 'Arguments = ' + self.Arguments + '\n'
        text += 'Queue {0:d}'.format(self.Queue)
        with open(configFile,'w') as f1:
            f1.write(text)
        return configFile

def test():
    mname = os.uname()[1].split('.')[0]
    if len(sys.argv)>1:
        print sys.argv
        return 0
    j1 = condorJob('outputs/test')
    j1.Executable = './condorJob.py'
    j1.Vars = 'outDir = outputs/test'
    j1.Arguments = '$(Process) $(outDir)'
    j1.jobTag = 't_$(Process)'
    j1.Queue = 5
    j1.submit("test1_cmd", False)

if __name__ == '__main__':
    test()
