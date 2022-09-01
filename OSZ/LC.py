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


COLOR_STYLE = ["red","green","blue","orange"]
Y_LABEL = r"B-Feld $B$ in $mT$"
X_LABEL = r"Abstand $s$ in $mm$"
SAVE_AS = "./OSZ/Tief.pdf"


U_e = 5.04
frequenz = getAxisEasy(18,6,"./OSZ/OSZ.xls","osz")
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
RC_u, errs = optimize.curve_fit(Durchlass,frequenz,g_a,p0=[100,2.3e-3,6.2e-9],epsfcn=1e-7)
print(minimize(Durchlass,Parameters(),"leastsq",args=(frequenz,g_a),epsfcn=1e-7))
print(RC_u)
RC_u= [100,2.3e-3,6.2e-9]
plot = genDataFromFunktion(10000,30000,55000,RC_u,arrDurchlass)
ax.scatter(frequenz,g_a,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[2],marker="o")
ax.plot(plot[0],plot[1])


fig, ax = plt.subplots()
ax.grid()
RC_ph, errs = optimize.curve_fit(Durchlass,frequenz,Pha,p0=[100,2.3e-3,6.2e-9] ,epsfcn=1e-7)#,p0=6.2e-9*4.7e3,bounds=[[6.2e-9*4.7e3],[0.00009]])
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