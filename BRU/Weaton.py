
from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties.unumpy  import uarray, nominal_values,std_devs
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Aufgabe 7  # Ungenauhig keit der Stommessung fehlt wie bringe ich die rein?
print("Aufgabe 7________________________________________________")
resistors =getAxisFromCell("A9","A12","./BRU/Mappe1.xls","wheaton")
poti = getAxisFromCell("B9","B12","./BRU/Mappe1.xls","wheaton")
print(resistors,poti)
uresistors = []
upoti = []
result = []
for i in range(len(resistors)):
    uresistors.append(uarray(resistors[i],resistors[i]*0.01))
    upoti.append(uarray(poti[i],analogErr(1)))
    result.append(upoti[i]/(1000-upoti[i])*uresistors[i])

print(uarrayToString(result))    
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

print(uarrayToString(result))   

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

print(uarrayToString(resWiederstand))   
print(uarrayToString(resI))
print(uarrayToString(resP))


#Aufgabe 10  # Ungenauhig keit der Stommessung fehlt wie bringe ich die rein?
print("Aufgabe 10_____________________________________________")
 
Spannung = arrToUnumpy([1,2,3,4,5,6],[1*0.005+0.008,2*0.005+0.08,3*0.005+0.08,4*0.005+0.08,5*0.005+0.08,6*0.005+0.08])
print(Spannung)
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
        #print(Spannung[j]/resWiederstand[j][i])
        resP[j].append(resWiederstand[j][i]*resI[j][i]*resI[j][i])

    print(uarrayToString(resWiederstand[j]))   
    print(uarrayToString(resI[j]))
    print(uarrayToString(resP[j]))

X_START =0
Y_START =12 
X_END = 4.2 
Y_END = 45.5 
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Wiederstand $U$ in $V$"
X_LABEL = r"Stromstärke in $I$ in $A$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 250
Y_MAJOR_TICK = 5 
X_MINOR_TICK = 50
Y_MINOR_TICK = 1
SAVE_AS = ""
COLOR_STYLE =["blue","red","green"]

numResWiederstand = np.rot90(np.array( [nominal_values(j).tolist() for j in [i for i in resWiederstand]]))

numResI = np.rot90(np.array( [nominal_values(j).tolist() for j in [i for i in resI]]))

print(numResWiederstand)
print(numResI)
fig, ax = plt.subplots()
ax.grid()
for i in range(len(numResI)):
    ax.scatter(numResI[i],numResWiederstand[i],s=10,linewidths=0.5,edgecolors="black",zorder=10,color = COLOR_STYLE[i])
ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)

# ax.set_xlim(X_START,X_END)
# ax.set_ylim(Y_START,Y_END)

# ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
# ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
# ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
# ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))
plt.show()
#fig.savefig(SAVE_AS)

