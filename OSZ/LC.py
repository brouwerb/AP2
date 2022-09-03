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
from lmfit import minimize,Parameters
from matplotlib.widgets import Slider


COLOR_STYLE = ["red","green","blue","orange"]
Y_LABEL = r"B-Feld $B$ in $mT$"
X_LABEL = r"Abstand $s$ in $mm$"
SAVE_AS = "./OSZ/Serie_durch.pdf"


U_e = 5.04
frequenz =   getAxisEasy(18,6,"./OSZ/OSZ.xls","osz")
U_a = getAxisEasy(18,7,"./OSZ/OSZ.xls","osz")
Pha = getAxisEasy(18,8,"./OSZ/OSZ.xls","osz")
g_a = [i / U_e for i in U_a]
print(frequenz,U_a,Pha)

def Durchlass(f,R,L,C):
    return R/np.sqrt(R**2+ (2 * np.pi * f * L- 1/(2 * np.pi * f *C ))**2)
def arrDurchlass(f,par):
    return Durchlass(f,par[0],par[1],par[2])

def Phase (f,R,L,C):
    return np.arctan(1/R * (2 * np.pi * f * L-1/(2 * np.pi * f *C ))) /np.pi *180
def arrPhase ( f,par):
    return Phase(f,par[0],par[1],par[2])


fig, ax = plt.subplots()
ax.grid()

plt.xscale("log")
RC_u, errs = optimize.curve_fit(Durchlass,frequenz,g_a,bounds =genIntBounds([100,2.3e-3,6.2e-9],1e-9))
#print(minimize(Durchlass,Parameters(),"leastsq",args=(frequenz,g_a)))

ax.scatter(frequenz,g_a,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[2],marker="o")


def change(Rvo,Rbi,Lvo,Lbi,Cvo,Cbi):
    popt,perr= optimize.curve_fit(Durchlass,frequenz,g_a,bounds=((Rvo,Lvo,Cvo),(Rbi,Lbi,Cbi)))
    #print(f"["+{popt}+","+{np.sqrt(np.diag(perr)) }+"]")
    print(np.sqrt(np.diag(perr)))
    
    xs,ys=genDataFromFunktion(1000,1000,100000,RC_u,arrDurchlass)
    ax.plot(xs,ys,color ="r")
    return ys


xs,ys=genDataFromFunktion(1000,1000,100000,RC_u,arrDurchlass)
[line] =ax.plot(xs,ys,color ="r")
von_ax1  = fig.add_axes([0.25, 0.175, 0.5, 0.03])
vonSl1 = Slider(von_ax1, 'f von', 1, 200 ,valinit=90)
bis_ax1  = fig.add_axes([0.25, 0.15, 0.5, 0.03])
bisSl1 = Slider(bis_ax1, 'f bis', 1, 200, valinit=110)

von_ax2  = fig.add_axes([0.25, 0.125, 0.5, 0.03])
vonSl2 = Slider(von_ax2, 'f von Sch', 1e-4,1e-2,valinit=2.1e-3)
bis_ax2  = fig.add_axes([0.25, 0.1, 0.5, 0.03])
bisSl2 = Slider(bis_ax2, 'f bis Sch',  1e-4,1e-2,valinit=2.6e-3)

von_ax3  = fig.add_axes([0.25, 0.075, 0.5, 0.03])
vonSl3 = Slider(von_ax3, 'amp von', 1e-9, 9e-9,valinit=6.0e-9)
bis_ax3  = fig.add_axes([0.25, 0.05, 0.5, 0.03])
bisSl3 = Slider(bis_ax3, 'amp bis', 1e-9, 9e-9,valinit=6.6e-9)

def sliders_on_changed(val):
    line.set_ydata(change(vonSl1.val,bisSl1.val,vonSl2.val,bisSl2.val,vonSl3.val,bisSl3.val))
    fig.canvas.draw_idle()
vonSl1.on_changed(sliders_on_changed)
bisSl1.on_changed(sliders_on_changed)
vonSl2.on_changed(sliders_on_changed)
bisSl2.on_changed(sliders_on_changed)
vonSl3.on_changed(sliders_on_changed)
bisSl3.on_changed(sliders_on_changed)













print(RC_u)
RC_u= [100,2.3e-3,6.2e-9]
plot = genDataFromFunktion(10000,30000,55000,RC_u,arrDurchlass)

#ax.plot(plot[0],plot[1])

plt.subplots_adjust(bottom=0.2)
fig, ax = plt.subplots()
ax.grid()
RC_ph, errs = optimize.curve_fit(Durchlass,frequenz,Pha,bounds =genIntBounds([100,2.3e-3,6.2e-9],1e-9))
print(RC_ph)
#RC_ph= [100,2.3e-3,6.2e-9]
plot = genDataFromFunktion(10000,100,100000,RC_ph,arrPhase)

ax.scatter(frequenz,Pha,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[2],marker="o")
ax.plot(plot[0],plot[1])


print("daraus folgt für die Grenz frequenzen:")
print(1/RC_u[0]/2/np.pi)
print(1/RC_ph[0]/2/np.pi)
plt.xscale("log")
plt.savefig(SAVE_AS)
plt.show()