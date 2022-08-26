from email import message
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
from scipy import optimize

X_START =0
Y_START =-50
X_END = 50
Y_END = 300
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Wiederstand $R$ in $\Omega$"
X_LABEL = r"Stromstärke in $I$ in $A$"

def func1(x,a,b,c):
    return a + b* x + c*x**2
def arrfunc1(x,a):
    return func1(x,a[0],a[1],a[2])
def func2(x,a,b,c,d):
    return a + b* x + c*x**2  + d * x**3
def arrfunc2(x,a):
    return func2(x,a[0],a[1],a[2],a[3])

funcs = [func2,func2,func2]
arrfuncs = [arrfunc2,arrfunc2,arrfunc2]
bounds = [[[-np.inf,-np.inf,-np.inf,-np.inf],[np.inf,np.inf,np.inf,np.inf]],[[-np.inf,-np.inf,-np.inf,0],[np.inf,np.inf,np.inf,0.0001]],
        [[-np.inf,-np.inf,-np.inf,-np.inf],[np.inf,np.inf,np.inf,np.inf]]]

messI = getAxisFromCell("B9","B35","./Vak/Vak.xls","Kalib")  
messP = getAxisFromCell("A9","A35","./Vak/Vak.xls","Kalib")  

plotRange= [[0,40],[15,50],[0,50]]

messI = [messI[:10],messI[7:18],messI[18:]]
messP = [messP[:10],messP[7:18],messP[18:]]
print(messP,messI)

fig, ax = plt.subplots()
ax.grid()
vals = [] 
for i in range(len(messI)):
    vals.append([])
    ax.scatter(messI[i],messP[i],s=20,linewidths=0.5,edgecolors="black",zorder=10)
    vals[i], errs = optimize.curve_fit(funcs[i],messI[i],messP[i],bounds = bounds[i])
    print(vals[i])
    plot = genDataFromFunktion(100,plotRange[i][0],plotRange[i][1],vals[i],arrfuncs[i])
    ax.plot(plot[0],plot[1])
    #ax.set_xlim(X_START,X_END)
    #ax.set_ylim(Y_START,Y_END)

plt.yscale("log")

plt.show()


