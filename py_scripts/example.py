#!/usr/bin/env python
from plotMaker import makeChain, plotMaker
# from rootUtil import useAtlasStyle, waitRootCmd, savehistory
from rootUtil import useAtlasStyle
from ROOT import TH1F

ch1 = makeChain('/net/s3_data_home/dzhang/links/outSpace/fourMuonsOut/xAug19a/fetch/data-myOutput/run304178-*.root', 'quad')
ch1.Show(0)

useAtlasStyle()
p1 = plotMaker(ch1, '')
opt = 'E'
p1.showVar(('m1P.pt', TH1F('h1','saveName;p_{T} [GeV];Events / 1 GeV', 50, 0, 50)), opt)
