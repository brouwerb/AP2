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


freq = getAxisEasy(2,1,"./TRA/TRA.xls","Tabelle2")
Ue = getAxisEasy(2,2,"./TRA/TRA.xls","Tabelle2")
Ua = getAxisEasy(2,3,"./TRA/TRA.xls","Tabelle2")
rawPha = getAxisEasy(2,4,"./TRA/TRA.xls","Tabelle2")

#print(freq,Ue,Ua,rawPha)
Pha = []
for i in range (len(freq)):
    if rawPha[i] == 180:
        buf = 180
    else:
        buf = 360 - (rawPha[i] *1e-6 * freq[i] * 360)
    Pha.append(buf)
#print(Pha)

COLOR_STYLE = ["red","green","blue","orange"]
Y_LABEL = r"Gain $U_{aus}/U_{ein} = A(f)$"
X_LABEL = r"Frequenz $f$ in Hz"
SAVE_AS = "./TRA/plots/Amplitudengang.pdf"

fig, ax = plt.subplots()
ax.grid()
# Amplitude = Uein / Uaus ????  bin mir nicht ganz sicher qber würde schon sinn ergeben
A = [Ua[i]/Ue[i] for i in range(len(Ue))]
ax.scatter(freq,A,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[0],marker="o", label="Messwerte")

Amax = np.max(np.array(A))
print(Amax , 1/np.sqrt(2) * Amax)
# Lösung 9.3
ax.axvspan(7,87600,color="orange",alpha= 0.3)
buf = "\n"
ax.annotate(rf"$A_{{max}}$ = {round(Amax,2)}",[freq[6],A[6]],xytext=[376,7.5],arrowprops=dict(arrowstyle="->",linewidth=1))
ax.annotate(rf"$\frac{{1}}{{\sqrt{{2}}}} \cdot A_{{max}}$ range {buf} 7 Hz - 87,6 kHz",[376,4.5],xytext=[300,4.5])

ax.set_xlabel(X_LABEL)
ax.set_ylabel(Y_LABEL)

plt.xscale("log")
plt.savefig(SAVE_AS)

fig, ax2 = plt.subplots()
ax2.grid()
Y_LABEL = r"Phase $\varphi(f)$ in °"
X_LABEL = r"Frequenz $f$ in Hz"
SAVE_AS = "./TRA/plots/Phasengang.pdf"

ax2.scatter(freq,Pha,s=15,linewidths=0.5,zorder=10,color = COLOR_STYLE[0],marker="o", label="Messwerte")

ax2.set_xlabel(X_LABEL)
ax2.set_ylabel(Y_LABEL)

plt.xscale("log")

plt.savefig(SAVE_AS)

plt.show()