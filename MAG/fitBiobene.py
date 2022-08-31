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
SAVE_AS = "./MAG/fit1.pdf"



def theo_kurve (x,I,R):
    mur = 1
    mu0 = 1.256e-6
    N = 1200
    return mur * mu0 * N / (2 * np.power((x)**2+ R**2,(3/2))) * R**2 * I
def arrtheo_kurve(x,a):
    return theo_kurve(x,a[0],a[1])


data = [[getAxisEasy(6,4+(j*3+i),"./MAG/Mag.xls","MAG") for i in range(3)] for j in range(5)]
dataWithErr = []
scaler = 0.001
for i in range(len(data)):
    dataWithErr.append([])
    dataWithErr[i].append(arrToUnumpyf([j*scaler for j in data[i][0]],[j*scaler*0.0025+digitalErr(0.5*scaler) for j in data[i][0]]))
    dataWithErr[i].append(arrToUnumpyf([j*scaler for j in data[i][1]],[np.sqrt((j*0.002*scaler)**2+(j*0.003*scaler)**2)+digitalErr(0.01*scaler) for j in data[i][1]]))
    dataWithErr[i].append(arrToUnumpyf([j*scaler for j in data[i][2]],[np.sqrt((j*0.002*scaler)**2+(j*0.003*scaler)**2)+digitalErr(scaler*scaler) for j in data[i][2]]))

#print(dataWithErr[0])
fig, ax = plt.subplots()
ax.grid()
difference = [[i[1][j]-i[2][j]  for j in range(len(i[1]))] for i in dataWithErr]
x_n , y_n = mirrorDataAroundX(2*scaler,nominal_values(dataWithErr[0][0]),nominal_values(difference[0]))
#print(x_n,y_n)
ax.scatter(x_n,y_n,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[0],marker="o")
#ax.errorbar(x_n,y_n,fmt="none",yerr=std_devs(difference[0]),xerr=std_devs(dataWithErr[0][0]),ecolor='black',elinewidth=0.8,capsize=2,capthick=0.8)

vals, errs = optimize.curve_fit(theo_kurve,x_n[12:],y_n[12:],bounds=[[0,0.01],[1.2,0.2]], method="dogbox")
print(vals)

plot = genDataFromFunktion(1000,-250*scaler,250*scaler,vals,arrtheo_kurve)

ax.plot(plot[0],plot[1])

ax.set_xlabel(X_LABEL)
ax.set_ylabel(Y_LABEL)
plt.savefig(SAVE_AS)
plt.show()

