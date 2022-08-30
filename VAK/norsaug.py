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

for col in [2, 6, 9, 12]:
    p = [kalibrierungsFunktion(j) for j in getAxisEasy(5, col-1, "./VAK/Vak.xls", "nr.4")]
    t = uarray(getAxisEasy(5, col, "./VAK/Vak.xls", "nr.4"), 0.1)
    print(p, t)