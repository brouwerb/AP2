
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
names = getAxisFromCell("A19","A24","./BRU/Mappe1.xls","wheaton")
print(resistors,poti)
uresistors = []
upoti = []
result = []
data8 = []
for i in range(len(resistors)):
    uresistors.append(uarray(resistors[i],resistors[i]*0.01))
    upoti.append(uarray(poti[i],analogErr(1)))
    result.append(upoti[i]/(1000-upoti[i])*uresistors[i])
    data8.append([names[i],round_err(float(nominal_values(upoti[i])), float(std_devs(upoti[i]))),round_err(float(nominal_values(result[i])), float(std_devs(result[i])))])

printtableaslatex(data8, "Wiederstand Spule in $\\si{\\ohm}$ und Vergleichswiderstand $10,00(10) \\si{\\ohm}$", ["Name", "Potieinstellung", "errechneter Widerstand"]) 
savetableastxt(data8, "Widerstand Spule in \\si{\\ohm} und Vergleichswiderstand 10,00(10) \\si{\\ohm}", "./BRU/wiespu", ["Name", "Potieinstellung", "errechneter Widerstand"])
#Aufgabe 9  # Ungenauhigkeit der Stommessung fehlt wie bringe ich die rein?
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
data9 = []
for i in range(len(resistors)):
    uresistors.append(uarray(resistors[i],resistors[i]*0.01))
    upoti.append(uarray(poti[i],analogErr(1)))
    resWiederstand.append(upoti[i]/(1000-upoti[i])*uresistors[i])
    resI.append(Spannung/resWiederstand[i])#
    resP.append(resWiederstand[i]*resI[i]*resI[i])
    





#Aufgabe 10  # Ungenauhig keit der Stommessung fehlt wie bringe ich die rein?
print("Aufgabe 10_____________________________________________")
 
Spannung = arrToUnumpy([1,2,3,4,5,6],[1*0.005+0.008,2*0.005+0.08,3*0.005+0.08,4*0.005+0.08,5*0.005+0.08,6*0.005+0.08])
#print(Spannung)
resistors =getAxisFromCell("A36","A39","./BRU/Mappe1.xls","wheaton")
poti = []
for i in range(1, len(Spannung)+1):
    poti.append(getAxis(35,i,38,"./BRU/Mappe1.xls","wheaton"))
print(poti)
#print(resistors,poti)
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
        uresistors[j].append(ufloat(resistors[i],resistors[i]*0.01))
        upoti[j].append(ufloat(poti[j][i],analogErr(1)))
        resWiederstand[j].append(upoti[j][i]/(1000-upoti[j][i])*uresistors[j][i])
        resI[j].append(Spannung[j]/(resWiederstand[j][i]+uresistors[j][i]))#
        #print(Spannung[j]/resWiederstand[j][i])
        resP[j].append(resWiederstand[j][i]*np.square(resI[j][i]))
        data9.append([Spannung[j], uresistors[j][i],upoti[j][i],resWiederstand[j][i],resI[j][i],resP[j][i]])

print(constructdata(resWiederstand))   
print(constructdata(resI))
print(constructdata(resP))

printtableaslatex(constructdata(data9), "Eigenschaften Glühlampe", ["Spannung in \\si{\\volt}", "Vergleichswiderstand in \\si{\\ohm}", "Potieinstellung in \\si{\\ohm}", "Widerstand Glühlampe in \\si{\\ohm}", "Strom in \\si{\\ampere}", "Leistung in \\si{\\watt}"])
savetableastxt(constructdata(data9), "Eigenschaften Glühlampe", "./BRU/eigglueh", ["$U$ in $\\si{\\volt}$", "$R_2$ in $\\si{\\ohm}$", "$Poti$ in $\\si{\\ohm}$", "$R_G$ in $\\si{\\ohm}$", "$I$ in $\\si{\\ampere}$", "$P$ in $\\si{\\watt}$"])

X_START =0
Y_START =0
X_END = 0.3 
Y_END = 15 
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Wiederstand $R$ in $\Omega$"
X_LABEL = r"Stromstärke in $I$ in $A$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 250
Y_MAJOR_TICK = 5 
X_MINOR_TICK = 50
Y_MINOR_TICK = 1
SAVE_AS = ""
COLOR_STYLE =["blue","red","green"]

numResWiederstand = np.rot90(np.array( [nominal_values(j).tolist() for j in [i for i in resWiederstand]]),3)
numResP = np.rot90(np.array( [nominal_values(j).tolist() for j in [i for i in resP]]),3)
numResI = np.rot90(np.array( [nominal_values(j).tolist() for j in [i for i in resI]]),3)
erResWiederstand = np.rot90(np.array( [std_devs(j).tolist() for j in [i for i in resWiederstand]]),3)
erResI = np.rot90(np.array( [std_devs(j).tolist() for j in [i for i in resI]]),3)
erResP = np.rot90(np.array( [std_devs(j).tolist() for j in [i for i in resP]]),3)

print(numResWiederstand)
print(numResI)
print(numResP)
fig, ax = plt.subplots()
ax.grid()
for i in range(len(numResI)):
    ax.errorbar(numResI[i],numResWiederstand[i],fmt="none",yerr=erResWiederstand[i],xerr=erResI[i],ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8,
        color=COLOR_STYLE[0],zorder=9)
    ax.scatter(numResI[i],numResWiederstand[i],s=20,linewidths=0.5,edgecolors="black",zorder=10,color = COLOR_STYLE[i])
ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)
ax.legend([r"R = 10$\Omega$",r"R = 30$\Omega$",r"R = 200$\Omega$"])
ax.set_xlim(X_START,X_END)
ax.set_ylim(Y_START,Y_END)

fig.savefig("./BRU/amp.pdf")

# ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
# ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
# ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
# ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))


Y_LABEL = r"Wiederstand $R$ in $\Omega$"
X_LABEL = r"Leistung $P$ in $mW$"

fig, ax2 = plt.subplots()
ax2.grid()
for i in range(len(numResI)):
    ax2.errorbar(np.array(numResP[i])*1e3,numResWiederstand[i],fmt="none",yerr=erResWiederstand[i],xerr=np.array(erResP[i])*1e3,ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8,
        color=COLOR_STYLE[0],zorder=9)
    ax2.scatter(np.array(numResP[i])*1e3,numResWiederstand[i],s=20,linewidths=0.5,edgecolors="black",zorder=10,color = COLOR_STYLE[i])
ax2.set(xlabel=X_LABEL, ylabel=Y_LABEL)
plt.yscale("log")
plt.xscale("log")
ax2.legend([r"R = 10$\Omega$",r"R = 30$\Omega$",r"R = 200$\Omega$"])
plt.show()
fig.savefig("./BRU/pow.pdf")