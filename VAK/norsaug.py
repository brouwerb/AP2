from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties.unumpy  import uarray, nominal_values,std_devs
from uncertainties import ufloat
from kalib import kalibrierungsFunktion
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from statistics import mean
sg = []
p = []
for col in [2, 6, 9, 12]:
    pv = [kalibrierungsFunktion(j)*100 for j in getAxisEasy(5, col-1, "./VAK/Vak.xls", "nr.4")]
    t = uarray(getAxisEasy(5, col, "./VAK/Vak.xls", "nr.4"), 1).tolist()
    print(t)
    pl = 957*100
    v = ufloat(80e-6, 1e-6)
    s = [(pl*v)/(pv[i]*t[i])*3600 for i in range(len(pv))]
    p.append(round(mean(pv), 1))
    sg.append(round_errtex(gewichteterMittelwert([nominal_values(i) for i in s], [std_devs(i) for i in s]), intExtFehler([nominal_values(i) for i in s], [std_devs(i) for i in s])))
    
data = [*zip(*[[str(i) for i in p], sg])]

savetableastxt(data, "Saugvermögen", "./VAK/saug", ["Druck in $\\si{\\pascal}$", "Saugleistung in $\\si{\\meter\\cubed\\per\\hour}$"])

print(data)