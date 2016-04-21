#!/usr/bin/env python
import os, sys, re
from subprocess import call
from ROOT import *
from rootUtil import useAtlasStyle, waitRootCmd, savehistory

def makeSafe(x):
    return re.sub('[^\]_','\_',x)

class slidesReport:
    ending = r'''\end{document}'''

    def __init__(self, filename='temp', title='A quick comparison', author=sys.argv[0], addOutline=False, aratio=None):
        self.filename = filename
        self.title = title
        self.author = author
        self.slides = ''
        self.cHeader = None
        self.addOutline = addOutline
        self.aratio = aratio
#         self.makeHeader()
    def makeHeader(self):
        self.header=r'\documentclass'
        if self.aratio: self.header+='[aspectratio='+self.aratio+']'
        self.header += r'''{beamer}
\usepackage[latin1]{inputenc}'''
        if self.cHeader: self.header += self.cHeader
        self.header += r'''
\usetheme{AnnArbor}
\title{'''+self.title+r'''}
\author{'''+self.author+r'''}
\institute{University of Michigan}
\date{\today}
\begin{document}

\begin{frame}
\titlepage
\end{frame}'''
        if self.addOutline: self.header += '\n'+r'''\begin{frame}
\frametitle{Table of Contents}
\tableofcontents[currentsection]
\end{frame}'''

        return self.header
    def addFigureSlide(self, title, figure, caption):
        self.slides += r'\begin{frame}{'+title.replace('_',r'\_')+r'''}
\begin{figure}
\centering
\includegraphics[width=0.8\textwidth]{'''+figure+'''}
\caption{'''+caption.replace('_',r'\_')+'''}
\end{figure}
\end{frame}'''

    def addMultiFigureSlide(self, title, figures, caption='', nFigPerRow=3, totalwidth=1.):
        self.slides += '\n'+r'\begin{frame}{'+title.replace('_',r'\_')+r'''}
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
        if caption: self.slides += '\n'+r'\caption{'+caption.replace('_',r'\_')+'}'
        self.slides += '\n'+r'\end{figure}'+'\n'+r'\end{frame}'

    def addSection(self, sectionname, addSectionPage=False):
        self.slides += '\n'+r'\section{'+sectionname.replace('_',r'\_')+'}'
        if addSectionPage: self.slides += '\n'+r'\frame{\sectionpage}'
    def report(self, filename=None, compile=True):
        if not filename: filename = self.filename
        if filename[-3:]!='.tex': filename+='.tex'
        with open(filename,'w') as f:
#             f.write(self.header+self.slides+self.ending)
            f.write(self.makeHeader()+self.slides+self.ending)
        if(compile): 
            call(['pdflatex', filename])
            call(['pdflatex', filename])

def setStyle(h, s):
    h.SetLineColor(s[0])
    h.SetLineWidth(s[1])
    h.SetLineStyle(s[2])
    h.SetMarkerColor(s[0])
    h.SetMarkerStyle(s[3])
    h.SetMarkerSize(s[4])

def saveCanvas(c,name):
    dname = os.path.dirname(name)
    print name, dname
    if not dname: os.makedirs(dname)
    c.SaveAs(name+'.eps')
#     c.SaveAs(name+'.png')
    c.SaveAs(name+'.pdf')

def savePad(args, c1=gPad):
    for arg in args if not isinstance(args, basestring) else [args]:
        if arg.find('.') != -1: gPad.SaveAs(arg)
        else:
            dname = os.path.dirname(arg)
            if dname:
                if not os.path.isdir(dname+'/png'):
                    os.makedirs(dname+'/png')
                arg1 = dname+'/png/'+os.path.basename(arg)
            c1.SaveAs(arg1+'.png')
            c1.SaveAs(arg+'.eps')
            c1.SaveAs(arg+'.pdf')


class fFileCompare:
    def __init__(self, flist=None, reporter=None):
        self.flist = flist if flist else []
        self.styles = {}
        self.reporter = reporter
        self.interactive = False
        self.m_fig_dir = ''
        self.m_figLogy = False
    def compare(self, f1, f2):
        self.flist = [f1, f2]
        self.compare()
    def addFile(self, f1):
        self.flist.append(f1)
    def compare(self):
        f0 = self.flist[0][0]
        next = TIter(f0.GetListOfKeys())
        while True:
            key = next()
            if not key: break
            obj = key.ReadObj()
            if obj.ClassName() == 'TTree':
                if self.reporter: self.reporter.addSection('TTree '+obj.GetName()+' Comparison')
                self.processTTree(obj.GetName())
            else:
                print 'Not supported type'
    def processTTree(self, treename):
        trs = [f[0].Get(treename) for f in self.flist]
        x = trs[0].GetListOfLeaves()
        for k in x:
            print k.ClassName(), k.GetName()

            oname = k.GetName()
            opt = 'Ehist'
            cut = ''
            norm = 'norm'
            i = 0
            lg = TLegend(0.7,0.8,0.92,0.94)
            for tr in trs:
                tr.Draw(oname,cut,opt+norm)
                h = gPad.GetPrimitive('htemp')
                h.SetName('h{0:d}'.format(i))
                setStyle(h, self.flist[i][2])
                if i==0: opt += 'same'
                lg.AddEntry(h, self.flist[i][1], 'lp')
                i += 1
            lg.SetFillStyle(0)
            lg.Draw()
            if self.m_figLogy: gPad.SetLogy()
            gPad.Update()
            if self.interactive: waitRootCmd()
            if self.reporter:
                if self.m_fig_dir!='' and self.m_fig_dir[-1] != '/': m_fig_dir+='/'
                doname = self.m_fig_dir+oname
                gPad.Update()
                savePad(doname)
                self.reporter.addFigureSlide(oname+' Comparison', doname, oname)


funlist=[]
def test():
    dir = os.getenv('SAMPLEDIR')
    a = fFileCompare()
    a.addFile((TFile(dir+'/muons_test/My_Dec_8_Zmumu.root','read'), 'Dec 8', (2,1,1,20,1)))
    a.addFile((TFile(dir+'/muons_test/My_Dec_16_Zmumu.root','read'), 'Dec 16', (4,1,1,25,1)))
    reporter = slidesReport()
    a.reporter = reporter
    a.interactive = False
    a.m_figLogy = True
    a.m_fig_dir = 'test1/'
    a.compare()
    reporter.report('testing', True)

#     waitRootCmd()
funlist.append(test)

if __name__ == '__main__':
    savehistory('.')
    useAtlasStyle()
    for fun in funlist: print fun()
