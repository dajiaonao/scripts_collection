#!/usr/bin/env python
import os, sys, re
from subprocess import call,Popen
from math import sqrt, ceil

def makeSafe(x):
    return re.sub('[^\]_','\_',x)

class Slide:
    def __init__(self):
        self.title = None
        self.points = []
        self.figures = []
        self.totalwidth = None
        self.nFigPerRow = None
        self.caption = None
        self.gometry = None

class slidesReport:
    ending = '\n\n'+r'''\end{document}'''

    def __init__(self, filename='temp', title='A quick comparison', author=sys.argv[0], addOutline=False, aratio=None):
        self.filename = filename
        self.title = title
        self.author = author
        self.slides = ''
        self.cHeader = None
        self.addOutline = addOutline
        self.aratio = aratio
        self.pageWidth = 1.
#         self.makeHeader()
    def makeHeader(self):
        self.header=r'\documentclass'
        if self.aratio: self.header+='[aspectratio='+self.aratio+']'
# \usepackage{slidesphysics}
        self.header += r'''{beamer}
\usepackage[latin1]{inputenc}'''
        if self.cHeader: self.header += self.cHeader
        self.header += r'''
\usetheme{CCNU}
\title{'''+self.title+r'''}
\author{'''+self.author+r'''}
\institute[CCNU]{Central China Normal University}
\date{\today}
\begin{document}

\begin{frame}
\titlepage
\end{frame}'''
        if self.addOutline: self.header += '\n\n'+r'''\begin{frame}
\frametitle{Table of Contents}
\tableofcontents[currentsection]
\end{frame}'''

        return self.header
    def addFigureSlide(self, title, figure, caption):
        self.slides += '\n\n'+r'\begin{frame}{'+title.replace('_',r'\_')+r'''}
\begin{figure}
\centering
\includegraphics[width=0.8\textwidth]{'''+figure+'''}
\caption{'''+caption.replace('_',r'\_')+'''}
\end{figure}
\end{frame}'''

    def addMultiFigureSlide(self, title, figures, captionOpt=None, nFigPerRow=3, totalwidth=None):
        if not totalwidth: totalwidth = self.pageWidth
        self.slides += '\n\n'+r'\begin{frame}{'+title.replace('_',r'\_')+r'''}
\begin{figure}
\centering'''
        inc_fig = r'\includegraphics[width='+'{0:.2f}'.format(totalwidth/nFigPerRow)+r'\textwidth]{'
        nInRow = 0
        for fig in figures:
            if nInRow == nFigPerRow:
                self.slides += r'\\'
                nInRow = 0
            self.slides += '\n'+inc_fig+fig+'}'
            nInRow += 1
        if captionOpt is None:
            if len(figures)==1: caption = figures[0]
            else: caption = ''
        else: caption = captionOpt
        if caption!='': self.slides += '\n'+r'\caption{'+caption.replace('_',r'\_')+'}'
        self.slides += '\n'+r'\end{figure}'+'\n'+r'\end{frame}'

    def addSlide(self, s):
        self.slides += '\n\n'+r'\begin{frame}'
        if s.title: self.slides += '{'+s.title.replace('_',r'\_')+'}'
        if s.points:
            self.slides += '\n'+r'\begin{itemize}'
            for p in s.points:
                self.slides += '\n'+r'\item '+p
            self.slides += '\n'+r'\end{itemize}'

        if len(s.figures) != 0:
            self.slides += r'''
\begin{figure}
\centering'''
            if not s.nFigPerRow: s.nFigPerRow = ceil(sqrt(len(s.figures)))
            totalwidth = s.totalwidth if s.totalwidth else self.pageWidth 
            inc_fig = r'\includegraphics[width='+'{0:.2f}'.format(totalwidth/s.nFigPerRow)+r'\textwidth]{'
            nInRow = 0
            for fig in s.figures:
                if nInRow == s.nFigPerRow:
                    self.slides += r'\\'
                    nInRow = 0
                self.slides += '\n'+inc_fig+fig+'}'
                print inc_fig
                print fig
                print self.slides
                nInRow += 1
            if s.caption: self.slides += '\n'+r'\caption{'+s.caption.replace('_',r'\_')+'}'
            self.slides += '\n'+r'\end{figure}'
        self.slides += '\n'+r'\end{frame}'


    def processFile(self, fname):
        with open(fname, 'r') as fin:
            s0 = None
            for line in fin.readlines():
                line = line.rstrip()
                if len(line)==0:
                    ###push
                    if s0:
                        self.addSlide(s0)
                        s0 = None
                    continue
                elif line[0] == '#': continue
                elif len(line)<2: continue

                ### create new slides
                if not s0: s0 = Slide()
                k = line[:2]
                x = line[2:]
                if k == 't:':
                    s0.title = x
                    print s0.title
                elif k == 'p:':
                    s0.points.append(x)
                elif k == 'g:':
                    s0.gometry = x
                elif k == 'w:':
                    s0.totalwidth = float(x)
                else: s0.figures.append(line)
            if s0:
                self.addSlide(s0)
                s0 = None

    def addSection(self, sectionname, addSectionPage=False):
        self.slides += '\n'+r'\section{'+sectionname.replace('_',r'\_')+'}'
        if addSectionPage: self.slides += '\n'+r'\frame{\sectionpage}'
    def report(self, filename=None, compile1=True):
        if not filename: filename = self.filename
        if filename[-3:]!='.tex': filename+='.tex'
        with open(filename,'w') as f:
#             f.write(self.header+self.slides+self.ending)
            f.write(self.makeHeader()+self.slides+self.ending)
        if compile1: 
            call(['pdflatex', filename])
            call(['pdflatex', filename])
        return filename.replace('.tex','.pdf')


# class fFileCompare:
#     def __init__(self, flist=None, reporter=None):
#         self.flist = flist if flist else []
#         self.styles = {}
#         self.reporter = reporter
#         self.interactive = False
#         self.m_fig_dir = ''
#         self.m_figLogy = False
#     def compare(self, f1, f2):
#         self.flist = [f1, f2]
#         self.compare()
#     def addFile(self, f1):
#         self.flist.append(f1)
#     def compare(self):
#         f0 = self.flist[0][0]
#         next = TIter(f0.GetListOfKeys())
#         while True:
#             key = next()
#             if not key: break
#             obj = key.ReadObj()
#             if obj.ClassName() == 'TTree':
#                 if self.reporter: self.reporter.addSection('TTree '+obj.GetName()+' Comparison')
#                 self.processTTree(obj.GetName())
#             else:
#                 print 'Not supported type'
#     def processTTree(self, treename):
#         trs = [f[0].Get(treename) for f in self.flist]
#         x = trs[0].GetListOfLeaves()
#         for k in x:
#             print k.ClassName(), k.GetName()
# 
#             oname = k.GetName()
#             opt = 'Ehist'
#             cut = ''
#             norm = 'norm'
#             i = 0
#             lg = TLegend(0.7,0.8,0.92,0.94)
#             for tr in trs:
#                 tr.Draw(oname,cut,opt+norm)
#                 h = gPad.GetPrimitive('htemp')
#                 h.SetName('h{0:d}'.format(i))
#                 setStyle(h, self.flist[i][2])
#                 if i==0: opt += 'same'
#                 lg.AddEntry(h, self.flist[i][1], 'lp')
#                 i += 1
#             lg.SetFillStyle(0)
#             lg.Draw()
#             if self.m_figLogy: gPad.SetLogy()
#             gPad.Update()
#             if self.interactive: waitRootCmd()
#             if self.reporter:
#                 if self.m_fig_dir!='' and self.m_fig_dir[-1] != '/': m_fig_dir+='/'
#                 doname = self.m_fig_dir+oname
#                 gPad.Update()
#                 savePad(doname)
#                 self.reporter.addFigureSlide(oname+' Comparison', doname, oname)
# 
# 
# funlist=[]
# def test1():
#     dir = os.getenv('SAMPLEDIR')
#     a = fFileCompare()
#     a.addFile((TFile(dir+'/muons_test/My_Dec_8_Zmumu.root','read'), 'Dec 8', (2,1,1,20,1)))
#     a.addFile((TFile(dir+'/muons_test/My_Dec_16_Zmumu.root','read'), 'Dec 16', (4,1,1,25,1)))
#     reporter = slidesReport()
#     a.reporter = reporter
#     a.interactive = False
#     a.m_figLogy = True
#     a.m_fig_dir = 'test1/'
#     a.compare()
#     reporter.report('testing', True)
# 
#     waitRootCmd()
# funlist.append(test1)

def main():
    ### -f figures list
    ### -c conf file
    ### -w and -W for 1610 and 169
    ### -g for figures alignment
    ### -k used to group figures
    ### -t separate for grouping
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-f', "--inputFigures", help="all input file", default=None)
    parser.add_option('-T', "--title", help="title of the slides", default='Quick Plots')
    parser.add_option('-c', "--inputConf", help="list of input file", default=None)
    parser.add_option('-o', "--output", help="direcotry for output files", default=None)
    parser.add_option("-w", "--wide1", action='store_true', default=False, help="use 16:10 size")
    parser.add_option("-W", "--wide2", action='store_true', default=False, help="use 16:9 size")
    parser.add_option('-m', "--mColumn", help="number of columun", type=int, default=1)
    parser.add_option('-n', "--nRow", help="number of rows", type=int, default=1)
    parser.add_option('-k', "--groupKey", help="grouping key", type=int, default=None)
    parser.add_option('-t', "--separator", help="grouping separator", default='_')
    parser.add_option("--width", help='page width', type=float, default=None)
    parser.add_option("--clean1", help='clean the temprary files', action='store_true', default=False)
    parser.add_option("--clean2", help='clean the all temprary files', action='store_true', default=False)
    parser.add_option("--oCmd", help='opening command', default='okular')
    parser.add_option('-N', "--noOpen", help="don't open pdf file when it's compiled", action='store_true', default=False)

    (options, args) = parser.parse_args()
#     print args
#     return

    ### input list
    if options.inputFigures: args += options.inputFigures.split(',')

    ### create doc
    output = 'test'
    if options.output: output = options.output
    elif options.inputConf: output = os.path.basename(options.inputConf).rstrip('.conf')

    s1 = slidesReport(output,options.title,'Dongliang Zhang')
    if options.wide1:
        s1.aratio = '1610'
    elif options.wide2:
        s1.aratio = '169'
    if options.width: s1.pageWidth = options.width
    nfig = options.mColumn * options.nRow

    ### group figures
    if options.groupKey:
        dict1 = {}
        for a in args:
            x1 = a.split(options.separator)
            try:
                dict1[x1[options.groupKey]].append(a)
            except KeyError:
                dict1[x1[options.groupKey]] = [a]
        print dict1
        for key,figs in dict1.iteritems():
            print figs
            figures = []
            for i in figs:
                x = i[:i.rfind('.')]
                if len(figures) == nfig:
                    s1.addMultiFigureSlide(key, figures, None, options.mColumn)
                    figures = []
                else:
                    figures.append(x)
    elif args:
#         print args
        figures = []
        for i in args:
            figures.append(i[:i.rfind('.')])
            print figures
            if len(figures) == nfig:
                s1.addMultiFigureSlide('', figures, None, options.mColumn)
                figures = []
        if figures:
            s1.addMultiFigureSlide('', figures, None, options.mColumn)

    ### configuration file
    if options.inputConf: s1.processFile(options.inputConf)

    ### finaly, compile the report
    pdfFile = s1.report()

    ### open the file if it's not opened yet and requested
    #     if not options.noOpen and os.path.isfile(pdfFile) and call(['pgrep', '-f', ' '.join(openCmd)])!=0 and which(openCmd[0]) is not None:
    if not options.noOpen:
        openCmd = [options.oCmd, pdfFile]
        if which(openCmd[0]) is None:
            print 'command', openCmd[0], 'does not exist'
            return
        if call(['pgrep', '-f', ' '.join(openCmd)])==0:
            print 'file', openCmd[1], 'probably is already opened with', openCmd[0], ', find/check/refersh your windows'
            print 'run `',' '.join(openCmd),'` to debug'
            return
        if not os.path.isfile(pdfFile):
            print 'file', openCmd[1], ' is not found. Check early (file production) processes'
            return
        print 'Opening file', openCmd[1], 'with', openCmd[0]
        Popen(openCmd)

def which(cmd):
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, cmd)):
                return os.path.join(path, cmd)
    return None


def findProcess(cmd='okular T2C.pdf'):
    return call(['pgrep', '-f', cmd])

if __name__ == '__main__':
    main()
