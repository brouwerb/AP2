from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties.unumpy  import uarray, nominal_values,std_devs
from uncertainties import ufloat
from kalib import kalibrierungsFunktion
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


rawTimes = [getAxisEasy(4,i,"./Vak/Vak.xls","nr.3")  for i in range(0,5,2)]
rawI = [getAxisEasy(4,i,"./Vak/Vak.xls","nr.3")  for i in range(1,6,2)]
rawP = [[kalibrierungsFunktion(j) for j in i] for i in rawI]
legende = ["Schlauch",r"Kapillare 3$mm$",r"Kapillare 2$mm$"]

print(rawTimes,rawP)
print([len(i) for i in rawTimes],[len(i) for i in rawP])

Y_LABEL = r"Druck $p$ in $mbar$"
X_LABEL = r"Zeit $t$ in $s$"
fig, ax = plt.subplots()
ax.grid()
for i in range(len(rawTimes)):
    ax.scatter(rawTimes[i],rawP[i],s=20,linewidths=0.5,edgecolors="black",zorder=10)
ax.set_xlabel(X_LABEL)
ax.set_ylabel(Y_LABEL)
ax.legend(legende)
plt.yscale("log")
plt.show()