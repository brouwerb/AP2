from inspect import getsourcefile
from opcode import hasjabs
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties.unumpy  import uarray, nominal_values,std_devs, umatrix
from uncertainties import ufloat
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

m = umatrix([[25e-3, 2e-3, 3e-3], [56e-2, 9.5e-2, 9.5e-2]], [[1e-3, 0.1e-3, 0.1e-3], [1e-2, 0.2e-2, 0.2e-2]])


Lv = (np.pi*np.power(m[0], 4))/(128*m[1]*1.82e-5)*5e2
Lk = 121*np.divide(np.power(m[0], 3), m[1])
d = m[0]
l = m[1]
Lv = Lv.tolist()[0]
Lk = Lk.tolist()[0]
Lv.append(1/(1/Lv[0]+1/Lv[1]))
Lk.append(1/(1/Lk[0]+1/Lk[1]))
Lv.append(1/(1/Lv[0]+1/Lv[2]))
Lk.append(1/(1/Lk[0]+1/Lk[2]))
print(Lv, Lk)
Lvs = uarrayToString(Lv)
Lks = uarrayToString(Lk)
Sv = []
Sk = []
for i in Lv:
    Sv.append(1/(360/3.5 + 1/i))
for i in Lk:
    Sk.append(1/(360/3.5 + 1/i))

Svs = uarrayToString(Sv)
Sks = uarrayToString(Sk)


data = [["Schlauch", "Kapillare 2mm", "Kapillare 3mm", "Schlauch + 2mm", "Schlauch + 3mm"], Lvs, Lks, Svs, Sks]

savetableastxt([*zip(*data)], "Theortische Werte", "./VAK/tabelle", ["Name", "L visk", "L mol", "S vis", "S mol"])

print(Lvs)
print(Lks)
