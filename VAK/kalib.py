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

rawmessI = getAxisFromCell("B9","B35","./Vak/Vak.xls","Kalib")  
rawmessP = getAxisFromCell("A9","A35","./Vak/Vak.xls","Kalib")  
errI = [0.1 for i in range(len(rawmessI))]
errP = [i * 0.2 + 0.002 / (2*np.sqrt(3)) for i in rawmessP]

plotRange= [[0,24.9],[24.9,37.6],[37.6,45]]


messI = [rawmessI[:10],rawmessI[10:18],rawmessI[18:]]
messP = [rawmessP[:10],rawmessP[10:18],rawmessP[18:]]
print(messP,messI)

Y_LABEL = r"Druck $p$ in $mbar$"
X_LABEL = r"Stromstärke in $I$ in $A$"

fig, ax = plt.subplots()
ax.grid()
vals = [] 
for i in range(len(messI)):
    vals.append([])
    ax.scatter(messI[i],messP[i],s=20,linewidths=0.5,edgecolors="black",zorder=10)
    ax.errorbar(messI[i],messP[i],fmt="none",yerr=errP[i],xerr=errI[i],ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8)
    vals[i], errs = optimize.curve_fit(funcs[i],messI[i],messP[i],bounds = bounds[i])
    print(vals[i])
    plot = genDataFromFunktion(100,plotRange[i][0],plotRange[i][1],vals[i],arrfuncs[i])
    ax.plot(plot[0],plot[1])
    ax.set_xlabel(X_LABEL)
    ax.set_ylabel(Y_LABEL)

def kalibrierungsFunktion(A):
    index = 0
    for I,i  in enumerate(plotRange):
        if i[0]<=A and A<=i[1]:
            index = I 
            break
    return arrfuncs[index](A,vals[index])
print(kalibrierungsFunktion(30))

def calcP(I):
    return I*I*41.6

plt.yscale("log")


fig, ax2 = plt.subplots()
ax2.grid()

X_LABEL = r"Druck $p$ in $mbar$"
Y_LABEL = r"Leistung $p$ in $\mu W$"


rawmessI_err= arrToUnumpyf (rawmessI,0.1)
r_zim = ufloat(42.6,digitalErr(0.1))
dataP = [i*i*r_zim for i in rawmessI_err]
druck = genDataFromFunktion(100,0,45,[],kalibrierungsFunktion)
arrP = genDataFromFunktion(100,0,45,[],calcP)
ax2.plot(druck[1],arrP[1])

ax2.scatter(rawmessP,[nominal_values(i) for i in dataP],s=20,linewidths=0.5,edgecolors="black",zorder=10)
ax2.errorbar(rawmessP,[nominal_values(i) for i in dataP],fmt="none",xerr=errP,yerr=[std_devs(i) for i in dataP],ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8)
plt.yscale("log")
plt.xscale("log")

ax2.set_xlabel(X_LABEL)
ax2.set_ylabel(Y_LABEL)

plt.show()
