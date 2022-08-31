from dataclasses import dataclass
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
from scipy import optimize


COLOR_STYLE = ["red","green","blue","orange"]
Y_LABEL = r"B-Feld $B$ in $mT$"
X_LABEL = r"Abstand $s$ in $mm$"
SAVE_AS = "./MAG/raw1.pdf"


data = [[getAxisEasy(6,4+(j*3+i),"./MAG/Mag.xls","MAG") for i in range(3)] for j in range(5)]
dataWithErr = []
for i in range(len(data)):
    dataWithErr.append([])
    dataWithErr[i].append(arrToUnumpyf(data[i][0],[j*0.0025+digitalErr(0.5) for j in data[i][0]]))
    dataWithErr[i].append(arrToUnumpyf(data[i][1],[np.sqrt((j*0.002)**2+(j*0.003)**2)+0.01 for j in data[i][1]]))
    dataWithErr[i].append(arrToUnumpyf(data[i][2],[np.sqrt((j*0.002)**2+(j*0.003)**2)+0.001 for j in data[i][2]]))


fig, ax = plt.subplots()
ax.grid()


difference = [[i[1][j]-i[2][j]  for j in range(len(i[1]))] for i in dataWithErr]

print(difference)

for i in range(len(data)-1):
    ax.scatter(data[i][0],data[i][1],s=15,linewidths=1.5,zorder=10,color = COLOR_STYLE[i],marker="+")
    ax.scatter(data[i][0],data[i][2],s=15,linewidths=1.5,zorder=10,color = COLOR_STYLE[i],marker = "x")
    ax.scatter(data[i][0],nominal_values(difference[i]),s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[i],marker="o")


    ax.errorbar(data[i][0],data[i][1],fmt="none",yerr=[np.sqrt((j*0.002)**2+(j*0.003)**2)+0.01 for j in data[i][0]],xerr=[j*0.0025+digitalErr(0.5) for j in data[i][0]],ecolor = 'black',elinewidth=0.4,capsize=2,capthick=0.4)
    ax.errorbar(data[i][0],data[i][2],fmt="none",yerr=[np.sqrt((j*0.002)**2+(j*0.003)**2)+0.001 for j in data[i][0]],xerr=[j*0.0025+digitalErr(0.5) for j in data[i][0]],ecolor = 'black',elinewidth=0.4,capsize=2,capthick=0.4)
    ax.errorbar(data[i][0],nominal_values(difference[i]),fmt="none",yerr=std_devs(difference[i]),xerr=[j*0.0025+digitalErr(0.5) for j in data[i][0]],ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8)

ax.legend(["Messwert","Untergrund","Differenz"])
ax.set_xlabel(X_LABEL)
ax.set_ylabel(Y_LABEL)
plt.savefig(SAVE_AS)
plt.show()


SAVE_AS = "./MAG/raw2.pdf"

fig, ax = plt.subplots()
ax.grid()

ax.scatter(data[3][0],data[3][1],s=15,linewidths=1.5,zorder=10,color = COLOR_STYLE[1],marker="x")
ax.scatter(data[3][0],data[3][2],s=15,linewidths=1.5,zorder=10,color = COLOR_STYLE[0],marker = "+")
ax.scatter(data[3][0],nominal_values(difference[3]),s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[2],marker="o")


ax.errorbar(data[3][0],data[3][1],fmt="none",yerr=[np.sqrt((j*0.002)**2+(j*0.003)**2)+0.01 for j in data[3][0]],xerr=[j*0.0025+digitalErr(0.5) for j in data[3][0]],ecolor = COLOR_STYLE[1],elinewidth=0.8,capsize=2,capthick=0.4)
ax.errorbar(data[3][0],data[3][2],fmt="none",yerr=[np.sqrt((j*0.002)**2+(j*0.003)**2)+0.001 for j in data[3][0]],xerr=[j*0.0025+digitalErr(0.5) for j in data[3][0]],ecolor = COLOR_STYLE[0],elinewidth=0.8,capsize=2,capthick=0.4)
ax.errorbar(data[3][0],nominal_values(difference[3]),fmt="none",yerr=std_devs(difference[3]),xerr=[j*0.0025+digitalErr(0.5) for j in data[3][0]],ecolor = COLOR_STYLE[2],elinewidth=0.8,capsize=2,capthick=0.8)

ax.legend(["Messwert","Untergrund","Differenz"])
ax.set_xlabel(X_LABEL)
ax.set_ylabel(Y_LABEL)

plt.savefig(SAVE_AS)
plt.show()
