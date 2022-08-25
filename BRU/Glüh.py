from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties import unumpy , ufloat
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import interpolate

auf2 = []
for i in range(35, 38):
    auf2.append(getRow(0,i,7, "./BRU/Mappe1.xls","wheaton"))

aufu2 = []
#Fehler: Probewiederstand x*0.01
# Ablesewiderstand = sqrt(1/(2*sqrt(3)) + (x*0.01)**2)
for i in auf2:
    aufu2.append(unumpy.uarray(i, [i[0]*0.01, sqrt(1/(2*sqrt(3))**2 + (i[1]*0.01)**2), sqrt(1/(2*sqrt(3))**2 + (i[2]*0.01)**2), sqrt(1/(2*sqrt(3)) + (i[3]*0.01)**2), sqrt(1/(2*sqrt(3)) + (i[4]*0.01)**2), sqrt(1/(2*sqrt(3)) + (i[5]*0.01)**2), sqrt(1/(2*sqrt(3)) + (i[6]*0.01)**2)]))

print(aufu2)



auf1 = []
for i in range(27, 31):
    auf1.append(getRow(0,i,2, "./BRU/Mappe1.xls","wheaton"))

aufu1 = []
for i in auf1:
    aufu1.append(unumpy.uarray(i, [i[0]*0.01, sqrt(1/(2*sqrt(3))**2 + (i[1]*0.01)**2)]))

def printtableaslatex(data, name, header, type):
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\begin{tabular}{|l|l|l|l|l|l|l|l|}")
    print("\\hline")
    print("\\textbf{"+header[0]+"} & \\textbf{"+header[1]+"} & \\textbf{"+header[2]+"} & \\textbf{"+header[3]+"} & \\textbf{"+header[4]+"} & \\textbf{"+header[5]+"} & \\textbf{"+header[6]+"} \\\\")
    print("\\hline")
    for i in range(len(data)):
        print(type[i], *data[i], sep=" & ", end="\\\\ \n")
    print("\\hline")
    print("\\end{tabular}")
    print("\\caption{"+name+"}")
    print("\\end{table}")

printtableaslatex(aufu2, "Ausgleichsgerade für den Bruch von $U_2$", ["$U_2$", "$R_2$", "$R_3$", "$R_4$", "$R_5$", "$R_6$", "$R_7$"], ["$U_2$", "$R_2$", "$R_3$", "$R_4$", "$R_5$", "$R_6$", "$R_7$"])
print(aufu1)