from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties.unumpy  import uarray, nominal_values,std_devs
from uncertainties import ufloat
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Aufgabe 11
verglInduktivi = ufloat(2.7e-3,0.1e-3)
hauptPoti=[[],[]]
nebenPoti = [[],[]]
print("Aufgabe 11________________________________________________")
spulenName =getAxisFromCell("A12","A15","./BRU/Mappe1.xls","kompwe")               # just the String
hauptPoti[0] = arrToUnumpy( getAxisFromCell("B12","B15","./BRU/Mappe1.xls","kompwe"),analogErr(1))
hauptPoti[1] = arrToUnumpy(getAxisFromCell("D12","D15","./BRU/Mappe1.xls","kompwe"),analogErr(1))
nebenPoti[0] = arrToUnumpy(getAxisFromCell("C12","C15","./BRU/Mappe1.xls","kompwe"),analogErr(0.2))
nebenPoti[1] = arrToUnumpy(getAxisFromCell("E12","E15","./BRU/Mappe1.xls","kompwe"),analogErr(0.2))

print(hauptPoti,nebenPoti)


# Aufgabe 13
testKond  = ufloat(1e-3,1e-3*0.05)
print("Aufgabe 13________________________________________________")
hauptPoti= arrToUnumpy(getAxisFromCell("B20","B22","./BRU/Mappe1.xls","kompwe") ,analogErr(1))  
nebenPoti= arrToUnumpy(getAxisFromCell("C20","C22","./BRU/Mappe1.xls","kompwe")   ,analogErr(0.2))



