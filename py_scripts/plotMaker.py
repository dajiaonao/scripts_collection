#!/usr/bin/env python
import os, sys, re
from ROOT import *
from rootUtil import useAtlasStyle, waitRootCmd, savehistory, get_default_fig_dir, useStyle1, useStyle2, useStyle

gROOT.LoadMacro('AtlasLabels.C')
from ROOT import ATLASLabel


funlist=[]
sDir = get_default_fig_dir()
sDirirectly=False

def makeChain(files, treename='tree2'):
    ch1 = TChain(treename)
    ch1.Add(files)
    return ch1

def logAxis(h1):
    if h1.GetTitle().find('_logy')!=-1:
        gPad.SetLogy()
    else: gPad.SetLogy(False)
    if h1.GetTitle().find('_logx')!=-1:
        gPad.SetLogx()
    else: gPad.SetLogx(False)


class plotMakerBase():
    def __init__(self):
        self.autoSave = sDirirectly
        self.sTag = 'pmTest_'
        self.sDir = sDir
        self.lt = TLatex()
        self.cmsInfo = '#sqrt{s} = 8 TeV, 20.3 fb^{-1}'
        self.sampleInfo = None
        self.showInfo = None
        self.keptHists = []
        self.keepHist = False

    def atlasLabel(self, label="Internal"):
        ylow = 0.82
        ATLASLabel(0.2,0.87,label,1,1)
        if self.cmsInfo: 
            myText(0.2,ylow,1,self.cmsInfo);
            ylow -= 0.07
        if self.sampleInfo:
            myText(0.2,0.75,1,self.sampleInfo);
            ylow -= 0.07
        if self.showInfo:
            self.lt.DrawLatexNDC(0.2, ylow, self.showInfo)


class plotMaker(plotMakerBase):
    def __init__(self, ch0, cut0):
        self.ch0 = ch0
        self.cut0 = cut0
        plotMakerBase.__init__(self)

        self.lastBinIncludeOverflow = False
        self.firstBinIncludeUnderflow = False
        self.legendHeader = None

    def checkOutOfRange(self, h1, renorm=False):
        nbins = h1.GetNbinsX()
        if self.lastBinIncludeOverflow:
            h1.SetBinContent(nbins, h1.GetBinContent(nbins)+h1.GetBinContent(nbins+1))
        if self.firstBinIncludeUnderflow:
            h1.SetBinContent(1, h1.GetBinContent(1)+h1.GetBinContent(0))
        if renorm: h1.Scale(1./h1.Integral(0,-1))

    def showVar(self, var1, opt=''):
        var = var1[0]
        h1 = var1[1]
        if opt.find('E')!=-1: h1.Sumw2()

        self.ch0.Draw(var+'>>'+h1.GetName(),self.cut0,opt)
        self.checkOutOfRange(h1, opt.find('norm')!=-1)

        logAxis(h1)
        self.atlasLabel()
        gPad.Update()
        waitRootCmd(sDir+self.sTag+h1.GetTitle(), self.autoSave)

    def show2D(self, var1, opt = 'colz'):
        gStyle.SetPadRightMargin(0.16)
        h1 = var1[1]
        hh1='>>h1' if opt.find('same')==-1 else ''
        self.ch0.Draw(var1[0]+hh1, self.cut0, opt)

        if self.keepHist: self.keptHists.append(h1)

        if opt.find('same')==-1:
            logAxis(h1)
            self.atlasLabel()
        gPad.Update()
        waitRootCmd(self.sDir+self.sTag+h1.GetTitle(), self.autoSave)
        gStyle.SetPadRightMargin(0.06)

    def stackCuts(self, var1s, cuts, opt='', doScale=False):
        var1 = var1s[0]
        h1 = var1s[1]

        lg1 = TLegend(0.7,0.8,0.92,0.94)
        lg1.SetFillStyle(0)
        h1.Sumw2()

        max1 = None
        i = 0
        hlist = []
        ts1 = THStack()
        for cut in cuts:
            hname = 'h'+cut[0]
            h2 = h1.Clone(hname)
            self.ch0.Draw(var1+'>>'+hname,cut[1],opt+'goff')
            useStyle(i,h2,True)
            self.checkOutOfRange(h2, opt.find('norm')!=-1)

            if doScale and len(cut)>3:
                h2.Scale(cut[3])
            ts1.Add(h2)
            lg1.AddEntry(h2, cut[2], 'f')
            i+=1

        ts1.Draw('hist')
        ts1.GetXaxis().SetTitle(h1.GetXaxis().GetTitle());
        ts1.GetYaxis().SetTitle(h1.GetYaxis().GetTitle());
#         hx.GetYaxis().SetRangeUser(0.01, max1*1.4)
        if self.legendHeader: lg1.SetHeader(self.legendHeader)
        lg1.Draw('same')
        logAxis(h1)

        self.atlasLabel()
        gPad.Update()
        waitRootCmd(self.sDir+self.sTag+h1.GetTitle(), sDirirectly)


    def compareCuts(self, var1s, cuts, opt='', doScale=False):
        ### cuts = [(tag, selection, legend, scale)]
        var1 = var1s[0]
        h1 = var1s[1]
        h1.Sumw2()

        olist = None
        if self.cut0:
            olist = self.ch0.GetEntryList()
            self.ch0.SetEntryList(0)
            print 'cut0 set, will apply this cut first as entrylist'
            self.ch0.Draw('>>elist', self.cut0, 'entrylist')
            elist = gDirectory.Get('elist')
            self.ch0.SetEntryList(elist)

        lg1 = TLegend(0.7,0.8,0.92,0.94)
        lg1.SetFillStyle(0)
        h1.Sumw2()

        max1 = None
        i = 0
        hlist = []
        for cut in cuts:
            hname = 'h'+cut[0]
            h2 = h1.Clone(hname)
            print cut[0], self.ch0.Draw(var1+'>>'+hname,cut[1],opt+'goff')
            useStyle(i,h2)
            self.checkOutOfRange(h2, opt.find('norm')!=-1)

            if doScale and len(cut)>3:
                h2.Scale(cut[3])
            max1 = h2.GetBinContent(h2.GetMaximumBin()) if max1==None else max(h2.GetBinContent(h2.GetMaximumBin()), max1)
            if i==0:
                hx = h2
                dopt='E'
            else:
                dopt = 'histsame'
            lg1.AddEntry(h2, cut[2], 'p' if dopt=='E' else 'l')
            h2.Draw(dopt)
            hlist.append(h2)
            i+=1
        hx.Draw('axisSAME')
        hx.GetYaxis().SetRangeUser(0.01, max1*1.4)
        lg1.Draw('same')
        logAxis(h1)

        self.atlasLabel()
        gPad.Update()
        waitRootCmd(self.sDir+self.sTag+h1.GetTitle(), sDirirectly)

        if olist:
            ch0.SetEntryList(olist)

    def compareChains(self, chs, var1s, opt=''):
        # chs: [(TChain, )]
        var1 = var1s[0]
        h1 = var1s[1]
        h1.Sumw2()

        ### compare same variable for differnt chains
        lg1 = TLegend(0.7,0.8,0.92,0.94)
        lg1.SetFillStyle(0)

        chs[0].Draw(var1+'>>h1', self.cut0, 'E')
        self.checkOutOfRange(h1, opt.find('norm')!=-1)

        lg1.AddEntry(h1, chs[0].GetTitle(), 'pl')

        max1 = h1.GetBinContent(h1.GetMaximumBin())
        i=1
        c = [0,0,2,4,3,6,7]
        for ch in chs[1:]:
            i+=1
            ch.Draw(var1,self.cut0,'same')
            hi = gPad.GetPrimitive('htemp')
            hi.SetName('h'+str(i))
            hi.SetLineColor(c[i])
            self.checkOutOfRange(hi, opt.find('norm')!=-1)

            max1 = max(hi.GetBinContent(hi.GetMaximumBin()),max1)
            lg1.AddEntry(hi, ch.GetTitle(), 'l')

        h1.GetYaxis().SetRangeUser(0.01, max1*1.2)
        logAxis(h1)

        lg1.Draw('same')

        self.atlasLabel()
        gPad.Update()
        waitRootCmd(self.sDir+self.sTag+h1.GetTitle(), sDirirectly)

    def compareVarsSimple(self, vars1, h1, opt=''):
        lg1 = TLegend(0.7,0.8,0.92,0.94)
        lg1.SetFillStyle(0)
        h1.Sumw2()

        self.ch0.Draw(vars1[0][0]+'>>h1', self.cut0, 'E'+opt)
        self.checkOutOfRange(h1,opt.find('norm')!=-1)

        lg1.AddEntry(h1, vars1[0][1], 'pl')
        max1 = h1.GetBinContent(h1.GetMaximumBin())

        i = 1
        for var1 in vars1[1:]:
            self.ch0.Draw(var1[0],self.cut0,opt+'same')
            h2 = gPad.GetPrimitive('htemp')
            h2.SetName('h2_'+str(i))
            useStyle(i,h2)
            self.checkOutOfRange(h1,opt.find('norm')!=-1)

            lg1.AddEntry(h2, var1[1], 'l')
            max1 = max(h2.GetBinContent(h2.GetMaximumBin()), max1)
            i+=1

        h1.GetYaxis().SetRangeUser(0.01, max1*1.2)
        lg1.Draw('same')
        if h1.GetTitle().find('_logy')!=-1:
            gPad.SetLogy()
        else: gPad.SetLogy(False)

        self.atlasLabel()
        gPad.Update()
        waitRootCmd(self.sDir+self.sTag+h1.GetTitle(), sDirirectly)

    def compareVars(self, vars1, h1, opt=''):
        ### vars1: [(tag1, lg1, [(var1a, cut1a),(var1b, cut1b)]), (tag2, lg2, [(var2, cut2)])]
        lg1 = TLegend(0.7,0.8,0.92,0.94)
        lg1.SetFillStyle(0)
        h1.Sumw2()

        max1 = None
        hists = []
        i = 0
        for var1 in vars1:
            h2name='h2_'+var1[0] ## use tag1
            h2 = h1.Clone(h2name)
            self.ch0.Draw(var1[2][0][0]+'>>'+h2name, self.cut0+var1[2][0][1], '')
            for v,c in var1[2][1:]:
                print v,c
                self.ch0.Draw(v+'>>+'+h2name, self.cut0+c, '')
            self.checkOutOfRange(h2,opt.find('norm')!=-1)
            useStyle(i,h2)
            lg1.AddEntry(h2, var1[1], 'l')
            hists.append(h2)
            max1 = h2.GetBinContent(h2.GetMaximumBin()) if max1==None else max(h2.GetBinContent(h2.GetMaximumBin()), max1)
            i+=1
        h1 = hists[0]
        h1.Draw('E')
        for h in hists[1:]: h.Draw(opt+'same')

        h1.GetYaxis().SetRangeUser(0.01, max1*1.2)
        lg1.Draw('same')
        if h1.GetTitle().find('_logy')!=-1:
            gPad.SetLogy()
        else: gPad.SetLogy(False)

        self.atlasLabel()
        gPad.Update()
        waitRootCmd(self.sDir+self.sTag+h1.GetTitle(), sDirirectly)
