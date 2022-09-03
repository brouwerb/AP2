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
frequenz =   getAxisEasy(18,6,"./OSZ/OSZ2.xls","osz")
U_a = getAxisEasy(18,7,"./OSZ/OSZ2.xls","osz")
Pha = getAxisEasy(18,8,"./OSZ/OSZ2.xls","osz")
g_a = [i / U_e for i in U_a]
print(frequenz,U_a,Pha)

def Durchlass(f, R, RL,f0):
    return RL*f*(2 * np.pi) / np.sqrt( (R*f*(2 * np.pi))**2 + ((f*(2 * np.pi))**2 - (f0*(2 * np.pi))**2)**2)
def arrDurchlass(f,par):
    return Durchlass(f,par[0],par[1], par[2])

def Phase (f,RL, f0):
    return ((2 * np.pi * f)**2 - (2 * np.pi * f0)**2)/(2*np.pi*f*RL)
def arrPhase ( f,par):
    return Phase(f,par[0],par[1])


fig, ax = plt.subplots()
ax.grid()

plt.xscale("log")
RC_u, errs = optimize.curve_fit(Durchlass,frequenz,g_a, bounds=[[-np.inf, -np.inf, 40e3], [np.inf, np.inf, 43e3]])
errs = np.sqrt(np.diag(errs))
#print(minimize(Durchlass,Parameters(),"leastsq",args=(frequenz,g_a)))
#p0 = [1.6e10, 42e3]
RC_u = RC_u.tolist()

ax.scatter(frequenz,g_a,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[0],marker="o", label = "Messwerte")

print(RC_u)

xs,ys=genDataFromFunktion(1000,10000,100000,RC_u,arrDurchlass)
[line] =ax.plot(xs,ys,color = COLOR_STYLE[1], label = f"Fit mit Rm/L = {round_errtex(RC_u[1], errs[1])}, R/L = {round_errtex(RC_u[0], errs[0])}, $\omega_0 = {round_errtex(RC_u[2]/1000, errs[2]/1000)} kHz$")



ax.legend()
plt.xscale("log")
plt.savefig("./OSZ/schwdurch.pdf")
plt.show()
# ax.plot(plot[0],plot[1],color = COLOR_STYLE[1], label = "Theoriekurve")

# plt.subplots_adjust(bottom=0.2)
fig, ax = plt.subplots()
ax.grid()
RC_ph, pherr = optimize.curve_fit(Phase,frequenz,[np.tan(i*2*np.pi/360) for i in Pha], p0 = [RC_u[0], 42e3], bounds = [[0, 40e3],[np.inf, 45e3]])
print(RC_ph)
RC_phe = np.sqrt(np.diag(pherr))
# #RC_ph= [100,2.3e-3,6.2e-9]
plot = genDataFromFunktion(10000,min(frequenz),max(frequenz),RC_ph,arrPhase)

ax.scatter(frequenz,Pha,s=15,linewidths=0.5,zorder=10,marker="o", label = "Messwerte", color = COLOR_STYLE[0])
ax.plot(plot[0], [np.arctan(i)*180/np.pi for i in plot[1]], label = f"Fit mit \\omega_0 = {round_errtex(RC_ph[1], RC_phe[1])}", color = COLOR_STYLE[0])

print("Eigenfrequenz Durch", round_errtex(RC_u[2]/1000, errs[2]/1000), "kHz")
print("Eigenfrequenz Phase", round_errtex(RC_ph[1]/1000, RC_phe[1]/1000), "kHz")
print("Durch", round_errtex(RC_u[0]/(2*np.pi), errs[0]/(2*np.pi)))
print("Phase", round_errtex(RC_ph[0]/(2*np.pi), RC_phe[0]/(2*np.pi)))

fd = ufloat(RC_u[2], errs[2])
fph = ufloat(RC_ph[1], RC_phe[1])
Bd = ufloat(RC_u[0]/(2*np.pi), errs[0]/(2*np.pi))
Bph = ufloat(RC_ph[0]/(2*np.pi), RC_phe[0]/(2*np.pi))

data = [["Eigenfrequenz $f_0$ in $\\si{\\kilo\\hertz}$", str(np.sqrt(1/(6.2e-9*2.2e-3))/(2*np.pi)), round_errtex(RC_u[2]/1000, errs[2]/1000),round_errtex(RC_ph[1]/1000, RC_phe[1]/1000)], ["Bandbreite $B_f$ in $\\si{\\ohm\\per\\henry}",str(100/2.2e-3), round_errtex(RC_u[0]/(2*np.pi), errs[0]/(2*np.pi)), round_errtex(RC_ph[0]/(2*np.pi), RC_phe[0]/(2*np.pi))], ["Güte", str(np.sqrt(2.2e-3/6.2e-9)/100), round_errtexU(fd/Bd), round_errtexU(fph/Bph)]]
print(data)

savetableastxt(data, "Schwingkreis Werte", "./OSZ/schw", ["Werte", "Theoretisch", "Durchlasskurve", "Phasenverschiebung"])

# print("daraus folgt für die Grenz frequenzen:")
# print(1/RC_u[0]/2/np.pi)
# print(1/RC_ph[0]/2/np.pi)
ax.legend()
plt.xscale("log")
plt.savefig("./OSZ/schwphase.pdf")
plt.show()