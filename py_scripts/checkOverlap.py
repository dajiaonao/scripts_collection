#!/usr/bin/python
import sys, os, string
if len(sys.argv) < 2:
    print 'Need at least 2 list. exit.'
    os.exit(1)
listFile1 = sys.argv[1]
listFile2 = sys.argv[2]
f1 = open(listFile1)
f2 = open(listFile2)
list10 = f1.readlines()
list20 = f2.readlines()
list1 = []
list2 = []
common = []
for i in list10:
#    j = i.lower()
    j=i
    list1.append(j)
for i in list20:
#    j = i.lower()
    j=i
    list2.append(j)
print len(list1), len(list2)
for i in range(len(list1)-1, -1, -1):
    value = list1[i]
    try:
        j = list2.index(value)
    except ValueError:
        print 'ValueError: ', value
        continue
    common.append(value)
    del list1[i]
    del list2[j]
print listFile1, len(list1), '\n----------------'
for i in list1:
    print i,
print
print listFile2, len(list2), '\n----------------'
for i in list2:
    print i,
print
# print 'common:', len(common), '\n----------------'
# for i in common:
#    print i,
