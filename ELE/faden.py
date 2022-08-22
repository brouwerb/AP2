from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties import unumpy  

B_Feld_I = unumpy.uarray(1.3,1.3*0.025+0.1)
Helm_R = unumpy.uarray(0.15,0.002)

col = ["A","D","G"]
radien = [0.03,0.04,0.05]
dataBKonst = []
for i in range (3):

    dataBKonst.append(getAxisFromCell(col[i]+"13",col[i]+"22","./ELE/data.xls","Faden"))
print(dataBKonst)
