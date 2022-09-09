from inspect import getsourcefile
import os.path as path, sys
from re import A
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties.unumpy  import uarray, nominal_values,std_devs
from uncertainties import ufloat
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from scipy import optimize

Ube =getAxisEasy(1,2,"./TRA/TRA.xls","Tabelle4")
Ib =getAxisEasy(1,3,"./TRA/TRA.xls","Tabelle4")


COLOR_STYLE = ["red","green","blue","orange"]
Y_LABEL = r"Current $I_B$ in $\mu A$"
X_LABEL = r"Voltage $U_{BE}$ in mV"
SAVE_AS = "./TRA/plots/Eingangskennlinie.pdf"

def exp1 (Ube,a,b):
    return a * np.exp(b*Ube)
def arrexp1 (Ube,a):
    return (exp1(Ube,a[0],a[1]))


fig, ax = plt.subplots()
ax.grid()

vals, errs = optimize.curve_fit(exp1,Ube,Ib, p0 = (1, 1e-6))
print(vals)
ax.scatter(Ube,Ib,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[0],marker="o", label="measurement")
plot = genDataFromFunktion(100,0,670,vals,arrexp1)
def arrTangente(x,a): # a in Form abl bei x0 , x0 , f(x0)
    return a[0]* (x-a[1])+a[2]
slope = vals[0]*vals[1]*np.exp(vals[1]*570)
tangente = genDataFromFunktion(100,450,670,[slope,570,arrexp1(570,vals)],arrTangente)
print("slope = ", slope)

ax.plot(plot[0],plot[1],label = "exponential fit")
ax.plot(tangente[0],tangente[1],color = "green", label = rf"tangent with slope = {round(slope,3)} $\frac{{mA}}{{V}}$ ")
ax.annotate("operating point",[570,arrexp1(570,vals)],xytext=[400,120],arrowprops=dict(arrowstyle="->",linewidth=1))
ax.legend()
ax.set_xlabel(X_LABEL)
ax.set_ylabel(Y_LABEL)
plt.savefig(SAVE_AS)

Ube =getAxisEasy(1,2,"./TRA/TRA.xls","Tabelle4")
Ib =getAxisEasy(1,3,"./TRA/TRA.xls","Tabelle4")


COLOR_STYLE = ["red","green","blue","orange"]
Y_LABEL = r"Current $I_C$ in $\mu A$"
X_LABEL = r"Voltage $U_{CE}$ in mV"
SAVE_AS = "./TRA/plots/Ausgangskennlinie.pdf"

Uce =getAxisEasy(1,6,"./TRA/TRA.xls","Tabelle4")
Ic = [getAxisEasy(1,7+i,"./TRA/TRA.xls","Tabelle4") for i in range(2)]

fig, ax = plt.subplots()
ax.grid()
labels = ["Ic uppwards", "Ic downwards"]
def exp2 (Uce,a,b):
    return a*(1-np.exp(-b*Uce))
def arrexp2 (Uce,a):
    return exp2(Uce,a[0],a[1])

for i in range(len(Ic)):
    vals,errs = optimize.curve_fit(exp2,Uce,Ic[i],p0 = (600,0.01))
    print(vals)
    slope = vals[0]*vals[1]*np.exp(-1*vals[1]*570)
    tangente = genDataFromFunktion(100,450,670,[slope,570,arrexp2(570,vals)],arrTangente)
    print("slope = ", slope)
    ax.plot(tangente[0],tangente[1],color = "black",zorder = 11)
    ax.scatter(Uce,Ic[i],s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[i],marker="o", label=labels[i])

    plot = genDataFromFunktion(100,0,1000,vals,arrexp2)
    ax.plot(plot[0],plot[1],color = COLOR_STYLE[i] ,linewidth = 1, label = "fit")
buf = "\n"
ax.annotate(rf"tangent around operating point {buf} slope = {exponentialNum(slope)} $\frac{{mA}}{{V}}$",[570,arrexp2(570,vals)],xytext=[360,320],arrowprops=dict(arrowstyle="->",linewidth=1))
ax.legend()
ax.set_xlabel(X_LABEL)
ax.set_ylabel(Y_LABEL)
plt.savefig(SAVE_AS)


plt.show()
