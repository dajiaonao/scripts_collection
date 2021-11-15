#!/usr/bin/env python3
import sys, re

inte = re.compile('^[-+]?\d+$')
flo  = re.compile('^[-+]?\d*\.\d*$')

def phaseArgs_v1():
    hd = []
    if len(sys.argv)==2 and sys.argv[1].find(':')!=-1: return ''

    Fi = 1
    for a in sys.argv[1:]:
        print("_{0}_".format(a))
        if inte.match(a) is not None:
            hd.append('F{0:d}I/I'.format(Fi))
        elif flo.match(a) is not None:
            hd.append('F{0:d}F/F'.format(Fi))
        else:
            hd.append('F{0:d}C/C'.format(Fi))
        Fi += 1
    return ':'.join(hd)

def phaseArgs():
    hd = []
    if len(sys.argv)==2 and sys.argv[1].find(':')!=-1: return ''

    Fi = 0
    for a in sys.argv[1:]:
        Fi += 1

        try:
            b = int(a)
            hd.append('F{0:d}I/I'.format(Fi))
            continue
        except ValueError:
            pass

        try:
            b = float(a)
            hd.append('F{0:d}F/F'.format(Fi))
            continue
        except ValueError:
            pass

        hd.append('F{0:d}C/C'.format(Fi))

    return ':'.join(hd)

if __name__ == '__main__':
    print(phaseArgs())
