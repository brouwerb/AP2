

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

CONST_VALUES = [[-3.07118987e-03, -1.39427396e-02,  5.05000184e-03,  4.57944220e-05],[ 7.89298710e+01, -6.33005411e+00,  1.31972234e-01,  1.86844591e-21],[-3.53538311e+04,  2.82391992e+03, -7.51870957e+01 , 6.67790107e-01]]

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

rawmessI = getAxisFromCell("B9","B35","./VAK/Vak.xls","Kalib")  
rawmessP = getAxisFromCell("A9","A35","./VAK/Vak.xls","Kalib")  
errI = [0.1 for i in range(len(rawmessI))]
errP = [i * 0.2 + 0.002 / (2*np.sqrt(3)) for i in rawmessP]

plotRange= [[0,24.9],[24.9,37.6],[37.6,45]]


messI = [rawmessI[:10],rawmessI[10:18],rawmessI[18:]]
messP = [rawmessP[:10],rawmessP[10:18],rawmessP[18:]]
#print(messP,messI)

Y_LABEL = r"Druck $p$ in $mbar$"
X_LABEL = r"Stromstärke in $I$ in $A$"
SAVE_AS = "./VAK/Kallibrierung.pdf"




if __name__ == "__main__":
    fig, ax = plt.subplots()
    ax.grid()
vals = [] 
for i in range(len(messI)):
    vals.append([])
    if __name__ == "__main__":
        ax.scatter(messI[i],messP[i],s=20,linewidths=0.5,edgecolors="black",zorder=10)
        ax.errorbar(messI[i],messP[i],fmt="none",yerr=errP[i],xerr=errI[i],ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8)
    if CONST_VALUES == []:
        vals[i], errs = optimize.curve_fit(funcs[i],messI[i],messP[i],bounds = bounds[i])
    else:
        vals[i]= CONST_VALUES[i]
    #print(vals[i])
    if __name__ == "__main__":
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

if __name__ == "__main__":
    def linFunc(x,a,b):
        return a*x+b
    def arrLinFunc(x,a):
        return linFunc(x,a[0],a[1])
    

    def calcP(I):
        return I*I*41.6

    plt.yscale("log")
    
    
    plt.savefig(SAVE_AS)
    plt.show()

    fig, ax2 = plt.subplots()
    ax2.grid()

    X_LABEL = r"Druck $p$ in $mbar$"
    Y_LABEL = r"Leistung $p$ in $\mu W$"
    SAVE_AS = "./VAK/Pp_Graph.pdf"
    trenner = 10

    rawmessI_err= arrToUnumpyf (rawmessI,0.1)
    r_zim = ufloat(42.6,digitalErr(0.1))
    dataP = [i*i*r_zim for i in rawmessI_err]
    druck = genDataFromFunktion(300,0.02,45,[],kalibrierungsFunktion)
    arrP = genDataFromFunktion(300,0.02,45,[],calcP)
    ax2.plot(druck[1],arrP[1])

    ax2.scatter(rawmessP,[nominal_values(i) for i in dataP],s=20,linewidths=0.5,edgecolors="black",zorder=10)
    ax2.errorbar(rawmessP,[nominal_values(i) for i in dataP],fmt="none",xerr=errP,yerr=[std_devs(i) for i in dataP],ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8)
    vals, errs = optimize.curve_fit(linFunc,rawmessP[:trenner],[nominal_values(i) for i in dataP][:trenner])
    buf = genDataFromFunktion(100,0,rawmessP[trenner],vals,arrLinFunc)
    ax2.plot(buf[0],buf[1],linestyle="--")
    print(vals)
    ax2.legend(["Graph aus Kallibrierungsfkt.","Messwerte",r"$ax + b$ mit $a=7433$ $b=913$"])
    plt.yscale("log")
    plt.xscale("log")
    ax2.set_ylim(500,1e5)
    ax2.set_xlim(0.025,300)
    ax2.set_xlabel(X_LABEL)
    ax2.set_ylabel(Y_LABEL)

  
    plt.savefig(SAVE_AS)
    plt.show()
