#!/usr/bin/env python
from ROOT import gROOT, gPad, TIter
import sys, os
class bcolors:
    '''Show colored messages:
    bcolors.show(LEWEL, TEXT)'''

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
    def show(self, level, text):
        try:
            print getattr(self, level) + text + self.ENDC
        except AttributeError as e:
            self.show('FAIL', e.args[0])
            print text

def get_default_fig_dir():
    from datetime import date
    return date.today().strftime('figs_%Y%b%d/')

def textValue(v, ndig=0):
    return ('{0:.'+'{0:d}'.format(ndig)+'f}').format(abs(v)).replace('.', 'm' if v<0 else 'p')

def get_pre(val):
    s = '{0:.3e}'.format(val).split('e')
    p = -int(s[1])
    if float(s[0]) < 3.55: p+=1
    if p<0: p=0
    return '{0:d}'.format(p)

def get_pre2(val):
    s = '{0:.3e}'.format(val).split('e')
    p = -int(s[1])+1
#     if float(s[0]) < 3.55: p+=1
    if p<0: p=0
    return '{0:d}'.format(p)

def to_precision(val):
    n=2
    s = '{0:.3e}'.format(val).split('e')
    p = -int(s[1])+n-1
    if p<0: p=0
    return ('{0:.'+'{0:d}'.format()+'f}').format(val)

def listContentOfPad(c1):
    next = TIter(c1.GetListOfPrimitives())
    while True:
        obj = next()
        if not obj: break
        print obj.ClassName(), obj.GetName(), obj.GetTitle()

def useStyle1(obj, mark=True):
    obj.SetLineColor(2)
    obj.SetLineWidth(2)
    if mark:
        obj.SetMarkerStyle(24)
        obj.SetMarkerColor(2)

def useStyle2(obj, mark=True):
    obj.SetLineColor(4)
    obj.SetLineWidth(2)
    if mark:
        obj.SetMarkerStyle(25)
        obj.SetMarkerColor(4)

def makeupHist(h1, lc, ls, lw, mc, ms, mz=1):
    h1.SetLineColor(lc)
    h1.SetLineStyle(ls)
    h1.SetLineWidth(lw)
    h1.SetMarkerColor(mc)
    h1.SetMarkerStyle(ms)
    h1.SetMarkerSize(mz)

def mkupHist(h1, t):
    h1.SetLineColor(t[0])
    h1.SetLineStyle(t[1])
    h1.SetLineWidth(t[2])
    h1.SetMarkerColor(t[3])
    h1.SetMarkerStyle(t[4])
    h1.SetMarkerSize(t[5])

def mkupHistSimple(h1, t):
    h1.SetLineColor(t[0])
    h1.SetLineStyle(t[1])
    h1.SetLineWidth(t[2])
    h1.SetMarkerColor(t[0])
    h1.SetMarkerStyle(t[3])

def waitRootCmd(defaultSaveName='test', saveDirectly=False):
    if saveDirectly: return savePad(defaultSaveName)

    code = 0
    while True:
        x = raw_input('root: ')
        if x.lower() == 'e' or x.lower() == 'end' or x.lower() == 'q' or x.lower() == 'quit' or x.lower() == '.q': sys.exit()
        elif x=='' or x.lower() == 'n' or x.lower() == 'next': break
        args = x.split()
        if args[0]=='s' or args[0]=='save':
            if len(args)<2: args.append(defaultSaveName)
            savePad(args[1:])
            code |= (1<<1)
            continue
        elif args[0]=='p' or args[0]=='pass': return args[1:]
        try:
            gROOT.ProcessLine(x)
        except:
            print 'command not recognized'
            continue
    return code

def waitRootCmdMore(padlist, saveDirectly=False):
    if saveDirectly:
        for p,c in padlist.iteritems():
            savePad(p, c)
    while True:
        x = raw_input('root: ')
        if x.lower() == 'e' or x.lower() == 'end' or x.lower() == 'q' or x.lower() == 'quit' or x.lower() == '.q': sys.exit()
        elif x=='' or x.lower() == 'n' or x.lower() == 'next': break
        args = x.split()
        if args[0]=='s' or args[0]=='save':
            if len(args)<2:
                for p,c in padlist.iteritems(): savePad(p, c)
            else: savePad(args[1:], gPad)
            continue
        try:
            gROOT.ProcessLine(x)
        except:
            print 'command not recognized'
            continue

def savePad(args, c1=gPad, saveC=False):
    for arg in args if not isinstance(args, basestring) else [args]:
        if arg.find('.') != -1: c1.SaveAs(arg)
        else:
            dname = os.path.dirname(arg)
            if not dname: dname = '.'
            if not os.path.isdir(dname+'/png'):
                os.makedirs(dname+'/png')
            arg1 = dname+'/png/'+os.path.basename(arg)
            c1.SaveAs(arg1+'.png')
            c1.SaveAs(arg+'.eps')
            c1.SaveAs(arg+'.pdf')
            if saveC: c1.SaveAs(arg+'.C')
    return 1

def setStyle(style):
    style.SetOptStat(0)
    style.SetPadTickX(1)
    style.SetPadTickY(1)
    style.SetOptTitle(0)
    style.SetPadTopMargin(0.02)
    style.SetPadRightMargin(0.02)
    style.SetPadBottomMargin(0.10)
    style.SetPadLeftMargin(0.10)

def useAtlasStyle():
    gROOT.LoadMacro("AtlasStyle.C")
    from ROOT import SetAtlasStyle
    SetAtlasStyle()

def savehistory(dir=os.environ["HOME"]):
    import rlcompleter, readline
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set show-all-if-ambiguous On')
 
    import atexit
    f = os.path.join(dir, ".python_history")
    try:
        readline.read_history_file(f)
    except IOError:
        pass
    atexit.register(readline.write_history_file, f)

if __name__ == '__main__':
    print 'test'
    tc = bcolors()
    tc.show('WARNING','testing')
    tc.show('blue','testing')
