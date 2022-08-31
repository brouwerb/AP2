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



data = [[getAxisEasy(6,4+(j*3+i),"./MAG/Mag.xls","MAG") for i in range(3)] for j in range(5)]
dataWithErr = []
for i in range(len(data)):
    dataWithErr.append([])
    dataWithErr[i].append(arrToUnumpyf(data[i][0],[j*0.0025+digitalErr(0.5) for j in data[i][0]]))
    dataWithErr[i].append(arrToUnumpyf(data[i][0],[np.sqrt((j*0.002)**2+(j*0.003)**2)+0.01 for j in data[i][0]]))
    dataWithErr[i].append(arrToUnumpyf(data[i][0],[np.sqrt((j*0.002)**2+(j*0.003)**2)+0.001 for j in data[i][0]]))
print(data)

fig, ax = plt.subplots()
ax.grid()

difference = [[i[1][j]-i[2][j]  for j in range(len(i[1]))] for i in data]
print(difference)

for i in range(len(data)-1):
    ax.scatter(data[i][0],data[i][1],s=15,linewidths=0.5,edgecolors="black",zorder=10,color = COLOR_STYLE[i],marker="+")
    ax.scatter(data[i][0],data[i][2],s=15,linewidths=0.5,edgecolors="black",zorder=10,color = COLOR_STYLE[i],marker = "x")
    ax.scatter(data[i][0],difference[i],s=15,linewidths=0.5,edgecolors="black",zorder=10,color = COLOR_STYLE[i],marker="o")


    ax.errorbar(data[i][0],data[i][1],fmt="none",yerr=[np.sqrt((j*0.002)**2+(j*0.003)**2)+0.01 for j in data[i][0]],xerr=[j*0.0025+digitalErr(0.5) for j in data[i][0]],ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8)
    ax.errorbar(data[i][0],data[i][2],fmt="none",yerr=[np.sqrt((j*0.002)**2+(j*0.003)**2)+0.001 for j in data[i][0]],xerr=[j*0.0025+digitalErr(0.5) for j in data[i][0]],ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8)
    ax.errorbar(data[i][0],difference[i],fmt="none",yerr=[dataWithErr[i],xerr=[j*0.0025+digitalErr(0.5) for j in data[i][0]],ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8)


plt.show()