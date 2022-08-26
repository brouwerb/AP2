from inspect import getsourcefile
from opcode import hasjabs
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
spuleRes = [ufloat(0.6157,0.0066),ufloat(0.3627,0.0043),ufloat(0.3199,0.0039)]
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
    # resR[i].append(1/hauptPoti[i][1]*(1000-hauptPoti[i][1])*(resR[i][0]-nebenPoti[i][1])) 
    # resL[i].append(1/hauptPoti[i][1]*(1000-hauptPoti[i][1])*resL[i][0])
    # resR[i].append(1/hauptPoti[i][2]*(1000-hauptPoti[i][2])*(resR[i][0]-nebenPoti[i][2])) 
    # resL[i].append(1/hauptPoti[i][2]*(1000-hauptPoti[i][2])*resL[i][0])
    resR[i].append(hauptPoti[i][1]/(1000-hauptPoti[i][1])*(resR[i][0]+nebenPoti[i][1])) 
    resL[i].append(hauptPoti[i][1]/(1000-hauptPoti[i][1])*resL[i][0])
    resR[i].append(hauptPoti[i][2]/(1000-hauptPoti[i][2])*(resR[i][0]+nebenPoti[i][2])) 
    resL[i].append(hauptPoti[i][2]/(1000-hauptPoti[i][2])*resL[i][0])

data= []
data.append(["Spule 1 R in \\si{\\ohm}"] +  uarrayToString(resR[0]))
data.append(["Spule 1 L in \\si{\\henry}"] +  uarrayToString(resL[0]))
data.append(["Spule 2 R in \\si{\\ohm}"] +  uarrayToString(resR[1]))
data.append(["Spule 2 L in \\si{\\henry}"] +  uarrayToString(resL[1]))
print (data)

savetableastxt(data,"Kompexe Widerstände der Spule", "./BRU/komp" , ["Messwert", "Vergleichsspule", "Spule EM", "Spule AM"])

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
resC =[]
print(hauptPoti,nebenPoti)
data = []
for i in range(len(hauptPoti)):
    resC.append((1000-hauptPoti[i])/hauptPoti[i]*testKond)
    data.append(["Kondensator " + str(i+1)] + uarrayToString([hauptPoti[i], resC[i]]))

savetableastxt(data,"Kapazität Kondensator", "./BRU/kond" , ["Kondensator", "Wert Poti in \\si{\\ohm}", "Kapazität C in \\si{\\farad}"])

print(uarrayToString(resC))

