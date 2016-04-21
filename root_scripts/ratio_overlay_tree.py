#!/usr/bin/env python
from ROOT import TChain, TCanvas, gROOT, gPad, gStyle, TLegend, TIter, TPaveText, TPad, TLine
import sys,os
from rootUtil import useAtlasStyle

import rlcompleter, readline
readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set show-all-if-ambiguous On')

import atexit
# f = os.path.join(os.environ["HOME"], ".python_history")
f = os.path.join(os.environ["HOME"], ".python_history")
try:
    readline.read_history_file(f)
except IOError:
    pass
atexit.register(readline.write_history_file, f)

def Usage():
     print 'Usage: '
     print '       end: end the program'
     print '       root COMMAND: run COMMAND in root'
     print '       var cut opt: compare distributions'

class bcolors:
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

def get_pre(val):
    s = '{0:.3e}'.format(val).split('e')
    p = -int(s[1])
    if float(s[0]) < 3.95: p+=1
    if p<0: p=0
    return '{0:d}'.format(p)

def listContentOfPad(c1):
    next = TIter(c1.GetListOfPrimitives())
    while True:
        obj = next()
        if not obj: break
        print obj.ClassName(), obj.GetName(), obj.GetTitle()

def addAlias(ch):
    ch.SetAlias('f1', 'cos(theta)*1')
    ch.SetAlias('f3', 'cos(theta)*f2')
    ch.SetAlias('f5', 'cos(theta)*f4')
    ch.SetAlias('f7', 'cos(theta)*f4*f2')
    ch.SetAlias('fa', 'sin(theta)*sin(theta1)*pow(sin(theta2),2)')
    ch.SetAlias('f8', 'fa*cos(phi1)')
    ch.SetAlias('f9', 'fa*sin(phi1)')
    ch.SetAlias('f10', 'fa*cos(phi1+2*phi2)')
    ch.SetAlias('f11', 'fa*sin(phi1+2*phi2)')
    ch.SetAlias('fb', 'sin(theta)*cos(theta1)*sin(theta2)*cos(theta2)')
    ch.SetAlias('f12', 'fb*cos(phi2)')
    ch.SetAlias('f13', 'fb*sin(phi2)')
    ch.SetAlias('fc', 'cos(theta)*sin(theta1)*sin(theta2)*cos(theta2)')
    ch.SetAlias('f14', 'fc*cos(phi1+phi2)')
    ch.SetAlias('f15', 'fc*sin(phi1+phi2)')
    ch.SetAlias('fd', 'sin(theta)*sin(theta2)*cos(theta2)')
    ch.SetAlias('f16', 'fd*cos(phi2)')
    ch.SetAlias('f17', 'fd*sin(phi2)')

latexMap = {'p':'Proton', 'pi':'Pion', 'mu1':'Muon1', 'mu2':'Muon2', 'pt':'p_{T} [MeV]', 'eta':'#eta', 'phi':'#phi [rad]'}

def latexVar(fi):
    out = fi
    if fi[0].lower() == 'f': out = 'F_{'+fi[1:]+'}'
    else:
        if not out.find('.') == -1:
            out = ''
            for i in fi.split('.'):
                if out != '': out += ' '
                out += latexMap[i]
    return out


if __name__ == '__main__':
    ch1 = TChain('anglesTree')
    ch2 = TChain('anglesTree')

    file_loc_common = os.getenv('SAMPLEDIR_LAMB')+'/2014Jan30/Jan30_2012_'
    ch1.Add(file_loc_common + 'b.root')
    ch2.Add(file_loc_common + 'bbar.root')

    tag1 = '#Lambda_{b}'
    tag2 = '#bar{#Lambda}_{b}'
    print tag1, ch1.GetEntries()
    print tag2, ch2.GetEntries()

    title = '2012'
    ch1.SetLineColor(2)
    ch1.SetMarkerColor(2)
    ch1.SetMarkerStyle(20)
    ch1.SetMarkerSize(0.8)
    ch2.SetLineColor(4)
    ch2.SetLineStyle(2)
    ch2.SetMarkerColor(4)
    ch2.SetMarkerSize(0.8)
    ch2.SetMarkerStyle(25)

    gStyle.SetOptStat(0)
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    colorful = bcolors()
    #colorful.disable()

    addAlias(ch1)
    addAlias(ch2)
    plotRatio = True
    useAtlasStyle()

    def runRoot(cmd):
        try:
            gROOT.ProcessLine(cmd)
        except RuntimeError as e:
            print colorful.FAIL, e, colorful.ENDC
            return False
        return True

    def colorOutChi2(value):
        colorcode = colorful.OKGREEN
        if value < 0.3173: colorcode = colorful.OKBLUE
        if value < 0.0455: colorcode = colorful.WARNING
        if value < 0.0027: colorcode = colorful.FAIL
        return [colorcode + 'Chi2 Test: ' + colorful.ENDC + '{0:.2g}'.format(value), '#chi^{2} test: '+'{0:.2g}'.format(value)]

    print '__Run your command__'
    cx = TCanvas('cx', 'cx')
    while True:
        x = raw_input('\033[1mCompare:\033[0m ')
        if x == 'end': break
        args = x.split()
        if len(args) < 2: Usage()
        elif args[0] == 'root': runRoot(x[5:])
        elif args[0] == 'save' or args[0] == 's':
            for name in args[1:]:
                if name.find('.')!=-1: cx.SaveAs(name)
                else:
                    cx.SaveAs(name+'.eps')
                    cx.SaveAs(name+'.pdf')
                    cx.SaveAs(name+'.png')
        elif args[0] == 'range' or args[0] == 'r':
            h1.GetYaxis().SetRangeUser(float(args[1]), float(args[2]))
            cx.Modified()
            cx.Update()
        elif len(args) < 3: Usage()
        else:
            var1 = args[0].replace('>>(', '>>htemp(')
            cut1 = args[1]
            opt1 = args[2]
            plotRatio = len(args) > 3 and args[3].lower() == 'r'
 
            var2 = args[0].split('>>')[0]
            #if opt1.find('prof') >= 0: var2 = var1
            cut2  = args[1]
            opt2 = opt1 + 'same'

            cx0 = cx
            cx1 = cx
            extra_scale = 1.3
            scale = (0.65/0.35)*extra_scale
            if plotRatio:
                cx0 = TPad("cx0", "cx0", 0, 0.35, 1, 1)
#                 print 'cx0:', cx0.GetCanvasID()
                cx1 = TPad("cx1", "cx1", 0, 0, 1, 0.35)
#                 print 'cx1:', cx1.GetCanvasID()
                cx0.SetBottomMargin(0);
                cx1.SetBottomMargin(0.4);
                cx0.Draw();
                cx1.SetTopMargin(0);
                cx1.Draw();
            cx0.cd()

            num1 = ch1.Draw(var1, cut1, opt1)
            print tag1, num1
            #h1 = gPad.GetPrimitive("htemp")
            h1 = gPad.GetListOfPrimitives().Last()
            try:
                h1.SetName('h1')
            except AttributeError as e:
                print colorful.FAIL, 'h1', e, colorful.ENDC
                continue
            h1.GetXaxis().SetTitle(latexVar(var2))
            h1.GetYaxis().SetTitle('Events')
            h1.GetYaxis().SetNdivisions(506);
            h1.GetXaxis().SetNdivisions(506);
            num2 = ch2.Draw(var2, cut2, opt2)
            print tag2, num2
            #h2 = gPad.GetPrimitive("htemp")
            h2 = gPad.GetListOfPrimitives().Last()
            try:
                h2.SetName('h2')
            except AttributeError as e:
                print colorful.FAIL, 'h2', e, colorful.ENDC
                continue
            if num1<0 or num2<0: continue
            #listContentOfPad(gPad)
            info_texts = []
            npre = get_pre(h1.GetMeanError())
            info_texts.append(tag1+': '+('{0:.'+npre+'f}#pm{1:.'+npre+'f}').format(h1.GetMean(), h1.GetMeanError()))
            npre = get_pre(h2.GetMeanError())
            info_texts.append(tag2+': '+('{0:.'+npre+'f}#pm{1:.'+npre+'f}').format(h2.GetMean(), h2.GetMeanError()))

            chi2Opt = 'UU' if opt1.find('norm') < 0 and opt1.find('prof') < 0 else 'WW'
            chi2Test = colorOutChi2(h2.Chi2Test(h1, chi2Opt))
            print chi2Test[0]
            info_texts.append(chi2Test[1])
            for t in info_texts: print t
            drawOpt = 'l' if opt1.find('E') < 0 else 'lp'
            lg = TLegend(0.75,0.75,0.95,0.85,title)
            lg.SetFillStyle(0)
            lg.SetBorderSize(0)
            lg.AddEntry(h1, tag1, drawOpt)
            lg.AddEntry(h2, tag2, drawOpt)
            lg.Draw('same')

            info = TPaveText(0.15, 0.70, 0.40, 0.85, 'NDC')
            info.SetBorderSize(0)
            info.SetFillStyle(0)
            for text in info_texts:
                t = info.AddText(text)
                t.SetTextAlign()
                t.SetTextFont(102)
            info.Draw()

            if plotRatio:
                h1c = h1.Clone('h1c')
                h1c.Divide(h2)
               
                cx1.cd()
                h1c.Draw()
                x_label = h1.GetXaxis().GetLabelSize();
                y_label = h1.GetYaxis().GetLabelSize();
                h1c.GetXaxis().SetLabelSize(x_label*scale);
                h1c.GetYaxis().SetLabelSize(y_label*scale);
                h1c.SetMarkerSize(1.0);
#                 xTitle = h1.GetXaxis().GetTitle();
#                 h1c.GetXaxis().SetTitle(xTitle);
                h1c.GetYaxis().SetTitle(tag1+"/"+tag2);
                h1c.GetYaxis().CenterTitle();
                x_t = h1.GetXaxis().GetTitleSize();
                y_t = h1.GetYaxis().GetTitleSize();
                y_o = h1.GetYaxis().GetTitleOffset();
                h1c.GetXaxis().SetTitleSize(x_t*scale);
                h1c.GetYaxis().SetTitleSize(y_t*scale);
                h1c.GetYaxis().SetTitleOffset(y_o/scale);
                h1c.GetYaxis().SetNdivisions(504);
             
                h1.GetXaxis().SetLabelSize(x_label*extra_scale);
                h1.GetYaxis().SetLabelSize(y_label*extra_scale);
                h1.GetXaxis().SetTitleSize(x_t*extra_scale);
                h1.GetYaxis().SetTitleSize(y_t*extra_scale);
                h1.GetYaxis().SetTitleOffset(y_o/extra_scale);

                l = TLine()
                l1 = l.DrawLine(h1c.GetXaxis().GetXmin(), 1., h1c.GetXaxis().GetXmax(), 1.)
                l1.SetLineStyle(2)
                l1.SetLineWidth(2)
 
            cx.Update()
            cx.cd()
            if len(args) > 3 and args[3] == ';':
                while True:
                    comm = raw_input('root: ')
                    runRoot(comm)
                    if comm == '' or comm[-1] != ';': break
                cx.Modified()
                cx.Update()
