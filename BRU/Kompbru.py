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
spuleRes = [ufloat(0.6157,66),ufloat(0.3627,43),ufloat(0.3199,39)]
hauptPoti=[[],[]]
nebenPoti = [[],[]]
resR = [[],[]]
resL = [[],[]]
print("Aufgabe 11________________________________________________")
spulenName =getAxisFromCell("A12","A15","./BRU/Mappe1.xls","kompwe")               # just the String


hauptPoti[0] = arrToUnumpyf(getAxisFromCell("B12","B15","./BRU/Mappe1.xls","kompwe"),analogErr(1))
hauptPoti[1] = arrToUnumpyf(getAxisFromCell("D12","D15","./BRU/Mappe1.xls","kompwe"),analogErr(1))
nebenPoti[0] = arrToUnumpyf(getAxisFromCell("C12","C15","./BRU/Mappe1.xls","kompwe"),analogErr(0.2))
nebenPoti[1] = arrToUnumpyf(getAxisFromCell("E12","E15","./BRU/Mappe1.xls","kompwe"),analogErr(0.2))
print(nebenPoti)
for i in range(len(hauptPoti)):   
    resR[i].append(hauptPoti[i][0]/(1000-hauptPoti[i][0])*(spuleRes[0]+nebenPoti[i][0])) 
    resL[i].append(hauptPoti[i][0]/(1000-hauptPoti[i][0])*verglInduktivi)
    resR[i].append(hauptPoti[i][1]/(1000-hauptPoti[i][1])*(resR[i][0]+nebenPoti[i][1])) 
    resL[i].append(hauptPoti[i][1]/(1000-hauptPoti[i][1])*resL[i][0])
    resR[i].append(hauptPoti[i][2]/(1000-hauptPoti[i][2])*(resR[i][0]+nebenPoti[i][2])) 
    resL[i].append(hauptPoti[i][2]/(1000-hauptPoti[i][2])*resL[i][0])




print("Wert d.Spule , Spule ME , Spule AM")
print("spule 1")
print(uarrayToString( resR[0]),uarrayToString(resL[0]))
print("spule 2")
print(uarrayToString( resR[1]),uarrayToString(resL[1]))


# Aufgabe 13
testKond  = ufloat(1e-3,1e-3*0.05)
print("Aufgabe 13________________________________________________")
hauptPoti= arrToUnumpyf(getAxisFromCell("B20","B22","./BRU/Mappe1.xls","kompwe") ,analogErr(1))  
nebenPoti= arrToUnumpyf(getAxisFromCell("C20","C22","./BRU/Mappe1.xls","kompwe")   ,analogErr(0.2))



