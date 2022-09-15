from dataclasses import dataclass
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

Rc = [i *1e3 for i in getAxisEasy(0,0,"./TRA/TRA.xls","RC_Auswertung")]
data=[]
bezeichner = ["mit Kond ohne Rl","ohne alles","mit allem"]
for i in range(3):
    data.append([[],[]])
    data[i][0] = getAxisEasy(0,1+i*2,"./TRA/TRA.xls","RC_Auswertung")
    data[i][1] = getAxisEasy(0,2+i*2,"./TRA/TRA.xls","RC_Auswertung")
print(Rc)
print(data)

COLOR_STYLE = ["red","green","blue","orange"]
Y_LABEL = r"Gain $U_{aus}/U_{ein}$"
X_LABEL = r"Collector resistance $R_C$ in ohm"

def linfunc (Rc,S,rce):
    return -S * 1/(1/Rc+1/rce)
def arrlinfunc (Rc,a):
    return linfunc(Rc,a[0],a[1])
def compfunc (Rc,Re,Rl):
    return - 1/(1/Rc+1/Rl)/Re
def arrcompfunc (Rc,a):
    return compfunc(Rc,a[0],a[1])

funcs = [linfunc,compfunc,linfunc]
arrfuncs = [arrlinfunc,arrcompfunc,arrlinfunc]
p0 = [[-0.022,1000],[-1044.63379101 , 479642.63383653],[-0.022,1000]]


Theo = [[-0.025,532e3],[ -1000 , 10000],[-0.025,9815]]
for i,I in enumerate(data):
    SAVE_AS = f"./TRA/plots/RC{i+1}.pdf"
    fig, ax = plt.subplots()
    ax.grid()
    A = [I[1][j]/I[0][j] for j in range(len(I[0]))]
    ax.scatter(Rc,A,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[0],marker="o", label="Measured Values")
    vals, errs = optimize.curve_fit(funcs[i],Rc,A,maxfev = 5000,p0=p0[i])

    print(vals)
    plot = genDataFromFunktion(100,0.1,10000,Theo[i],arrfuncs[i])
    ax.plot(plot[0],plot[1],color= "blue", label="theoretical curve")
    ax.set_xlabel(X_LABEL)
    ax.set_ylabel(Y_LABEL)
    ax.set_xlim(0,10500)
    plt.legend()
    plt.savefig(SAVE_AS)
plt.show()




