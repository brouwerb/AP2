
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties.unumpy  import uarray, nominal_values,std_devs
from uncertainties import ufloat


# Aufgabe 7  # Ungenauhig keit der Stommessung fehlt wie bringe ich die rein?
print("Aufgabe 7________________________________________________")
resistors =getAxisFromCell("A9","A12","./BRU/Mappe1.xls","wheaton")
poti = getAxisFromCell("B9","B12","./BRU/Mappe1.xls","wheaton")

uresistors = []
upoti = []
result = []
data7 = []
for i in range(len(resistors)):
    uresistors.append(ufloat(resistors[i],resistors[i]*0.01))
    upoti.append(ufloat(poti[i],analogErr(1)))
    result.append(upoti[i]/(1000-upoti[i])*uresistors[i])
    data7.append([uresistors[i],upoti[i],result[i]])

printtableaslatex(constructdata(data7), "Wirderstand Poti", ["Vergleichswiderstand", "Potieinstellung", "errechneter Widerstand"])
savetableastxt(constructdata(data7), "Wiederstand Poti in \\si{\\ohm}", "./BRU/wiepo", ["Vergleichswiderstand", "Potieinstellung", "errechneter Widerstand"])
# Aufgabe 8   # Ungenauhig keit der Stommessung fehlt wie bringe ich die rein?
print("Aufgabe 8________________________________________________")
resistors =getAxisFromCell("B19","A24","./BRU/Mappe1.xls","wheaton")
poti = getAxisFromCell("C19","C24","./BRU/Mappe1.xls","wheaton")
print(resistors,poti)
uresistors = []
upoti = []
result = []
for i in range(len(resistors)):
    uresistors.append(uarray(resistors[i],resistors[i]*0.01))
    upoti.append(uarray(poti[i],analogErr(1)))
    result.append(upoti[i]/(1000-upoti[i])*uresistors[i])

print(uarrrayToString(result))   

#Aufgabe 9  # Ungenauhig keit der Stommessung fehlt wie bringe ich die rein?
print("Aufgabe 9________________________________________________")
resistors =getAxisFromCell("A28","A32","./BRU/Mappe1.xls","wheaton")
poti = getAxisFromCell("B28","B32","./BRU/Mappe1.xls","wheaton")
print(resistors,poti)
uresistors = []
upoti = []
resWiederstand = []
resI = []
resP = []
Spannung = uarray(1,1*0.005+0.008)    
for i in range(len(resistors)):
    uresistors.append(uarray(resistors[i],resistors[i]*0.01))
    upoti.append(uarray(poti[i],analogErr(1)))
    resWiederstand.append(upoti[i]/(1000-upoti[i])*uresistors[i])
    resI.append(Spannung/resWiederstand[i])#
    resP.append(resWiederstand[i]*resI[i]*resI[i])

print(uarrrayToString(resWiederstand))   
print(uarrrayToString(resI))
print(uarrrayToString(resP))


#Aufgabe 10  # Ungenauhig keit der Stommessung fehlt wie bringe ich die rein?
print("Aufgabe 10_____________________________________________")
 
Spannung = arrToUnumpy([1,2,3,4,5,6],[1*0.005+0.008,2*0.005+0.08,3*0.005+0.08,4*0.005+0.08,5*0.005+0.08,6*0.005+0.08])
resistors =getAxisFromCell("A36","A39","./BRU/Mappe1.xls","wheaton")
poti = []
for i in range(len(Spannung)):
    poti.append(getAxis(35,i,38,"./BRU/Mappe1.xls","wheaton"))
print(resistors,poti)
uresistors = [] 
upoti = []
resWiederstand = []
resI = []
resP = []
for j in range(len(Spannung)):
    uresistors.append([])
    upoti.append([])
    resWiederstand.append([])
    resI.append([])
    resP.append([])
    for i in range(len(resistors)):
        uresistors[j].append(uarray(resistors[i],resistors[i]*0.01))
        upoti[j].append(uarray(poti[j][i],analogErr(1)))
        resWiederstand[j].append(upoti[j][i]/(1000-upoti[j][i])*uresistors[j][i])
        resI[j].append(Spannung[j]/resWiederstand[j][i])#
        resP[j].append(resWiederstand[j][i]*resI[j][i]*resI[j][i])

    print(uarrrayToString(resWiederstand[j]))   
    print(resI[0][j])
    print(uarrrayToString(resP[0][j]))