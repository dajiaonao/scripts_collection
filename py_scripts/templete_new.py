#!/usr/bin/env python3
import os, sys, re
from ROOT import gROOT
from rootUtil3 import useAtlasStyle, waitRootCmd, savehistory, mkupHistSimple, get_default_fig_dir
funlist=[]

sDir = get_default_fig_dir()
sTag = 'test_'
sDirectly = False
if gROOT.IsBatch(): sDirectly = True

def test():

    return "In test"

    waitRootCmd()
funlist.append(test)

if __name__ == '__main__':
    savehistory('.')
    useAtlasStyle()
    for fun in funlist: print(fun())
