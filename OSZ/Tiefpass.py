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
SAVE_AS = "./OSZ/Tief.pdf"


U_e = 4.96
frequenz = getAxisEasy(8,0,"./OSZ/OSZ.xls","osz")
U_a = getAxisEasy(8,1,"./OSZ/OSZ.xls","osz")
Pha = getAxisEasy(8,2,"./OSZ/OSZ.xls","osz")
g_a = [i / U_e for i in U_a]
print(frequenz,U_a,Pha)

def Durchlass(f,par):
    return 1/np.sqrt(1+ (2 * np.pi * f * par)**2)
def arrDurchlass(f,par):
    return Durchlass(f,par[0])

def Phase (f,par):
    return np.arctan(2 * np.pi * f * par) /np.pi *180
def arrPhase ( f,par):
    return Phase(f,par[0])


fig, ax = plt.subplots()
ax.grid()

plt.xscale("log")
RC_u, errs = optimize.curve_fit(Durchlass,frequenz,g_a, bounds = [[0], [np.inf]])
print(RC_u)
RC = round_errtex(RC_u[0],errs[0])
plot = genDataFromFunktion(10000,100,100000,RC_u,arrDurchlass)
ax.scatter(frequenz,g_a,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[2], marker="o", label = "Messwerte")
ax.plot(plot[0],plot[1], color = COLOR_STYLE[0], label = f"Fit mit RC = {RC} Ohm Farad")
ax.legend()

plt.savefig("./OSZ/Tiefdurch.pdf")
plt.show()

fig, ax = plt.subplots()
ax.grid()
RC_ph, errs = optimize.curve_fit(Durchlass,frequenz,Pha,p0=6.2e-9*4.7e3,bounds=[[6.2e-9*4.7e3],[0.00009]])
print(RC_ph)
plot = genDataFromFunktion(10000,100,100000,RC_ph,arrPhase)

ax.scatter(frequenz,Pha,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[2],marker="o")
ax.plot(plot[0],plot[1])


print("daraus folgt für die Grenz frequenzen:")
print(1/RC_u[0]/2/np.pi)
print(1/RC_ph[0]/2/np.pi)
plt.xscale("log")
plt.savefig(SAVE_AS)
plt.show()