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
from matplotlib.ticker import MultipleLocator
from scipy import optimize
from lmfit import minimize,Parameters
from matplotlib.widgets import Slider



t = getAxisEasy(34,2,"./OSZ/OSZ2.xls","osz")
Up = getAxisEasy(34,1,"./OSZ/OSZ2.xls","osz")
u = [abs(i) for i in Up]

def expfit(t, A, tau):
    return A * np.exp(-t*tau)

def arrExpfit(t,par):
    return expfit(t,par[0],par[1])

popt, pconv = optimize.curve_fit(expfit, t, u, bounds=[[-np.inf, 0], [np.inf, np.inf]])
print(popt, t, u)
err = np.sqrt(np.diag(pconv))


tm = np.linspace(0, 100, 1000)


fig, ax = plt.subplots()
plt.rcParams['text.usetex'] = True
ax.grid()
ax.plot(tm, [expfit(i, *popt) for i in tm], 'r-', label= f'Fit mit $\\delta$ = {round_errtex(popt[1]*1e6,err[1]*1e6)} 1/s')
ax.scatter(t, u, color = 'green', marker = "o", label = "Messwerte")
plt.yscale('log')
plt.ylabel(r"U in mV")
plt.xlabel("t in $\\mu s$")
print(round_errtex(popt[1]*1e6,err[1]*1e6))
plt.savefig("./OSZ/expfit2.pdf")
ax.legend()
plt.show()

