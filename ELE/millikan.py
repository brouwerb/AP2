from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties import unumpy  

#Unsere Daten
col = ["A","B","C"]
data = []
for i in range(8, 33):
    data.append(getRow(0,i,3, "./ELE/data.xls","Millikan") + [0.5*(7.57-3.72)*10e-3])

#import data from txt file
with open("./ELE/datamoodle.txt") as f:
    for line in f:
        row = line.split()
        data.append([float(row[1].replace(",",".")),float(row[3].replace(",",".")),float(row[2].replace(",",".")),float(row[0].replace(",","."))])

print(data)

