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

#Unsere Daten
col = ["A","B","C"]
data = []
for i in range(8, 33):
    data.append(getRow(0,i,3, "./ELE/data.xls","Millikan") + [0.5*(7.57-3.72)*1e-3])

unsere_daten = len(data)

#tommys Daten
for i in range(5, 26):
    row = getRow(0,i,3, "./ELE/tommy.xls","Tabelle1")
    data.append([row[2], row[1], row[0], 0.5*(3.55)*1e-3])

tommys_daten = len(data)


#import data from txt file
with open("./ELE/datamoodle.txt") as f:
    for line in f:
        row = line.split()
        data.append([float(row[1].replace(",",".")),float(row[3].replace(",",".")),float(row[2].replace(",",".")), float(row[0].replace(",","."))])

sass_date = len(data)

#Unsicherheiten:
#Spannung: 1/(2*sqrt(3))
#Zeit: Ablese sprt((0.1/(2*sqrt(3)))**2 + 0.4) Reaktions 0.2
#Abstand: 0.5*10e-3/(2*sqrt(3))

udata = unumpy.umatrix(data, [[1/(2*sqrt(3)), sqrt((0.1/(2*sqrt(3)))**2 + 0.4), sqrt((0.1/(2*sqrt(3)))**2 + 0.4), 0.5e-3/(2*sqrt(3))]])

umat = udata.transpose()

# Viskosität Luft http://www.peacesoftware.de/einigewerte/luft.html bei 1 bar und 24°C: 18.4304*10e-6
nl = 18.4304e-6
#Dichte Öl = 871 kg/m³
#Dichte Luft = 1.17228 kg/m³ http://www.peacesoftware.de/einigewerte/luft.html

drho = 871 - 1.17228

# s = vt  v = s/t
vst = np.squeeze(np.divide(umat[3],umat[1]))
vsi = np.squeeze(np.divide(umat[3],umat[2]))

r0 = (3/2)*unumpy.sqrt((nl*(vst + vsi)/drho/9.8072914)) #https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjrtI2vstv5AhVfQvEDHUCBChMQFnoECAQQAQ&url=https%3A%2F%2Fwww.uni-kassel.de%2Ffb10%2Findex.php%3FeID%3DdumpFile%26t%3Df%26f%3D2720%26token%3Dd35b3b1bc0149f09f203a8d91bdbf963e8108572&usg=AOvVaw0pgyv1jNUF-dF_znxzshgh


#Nach skript:
A = 1.257
lam = ufloat(72, 2)*1e-9

rkorr = np.squeeze(unumpy.sqrt(np.multiply(r0,r0) + A**2*lam**2/4) - A*lam/2)

nlkorr = nl/(1 + A*lam/r0)

d = ufloat(0.006, 0.00005)

q = 3*np.pi*d*np.divide(np.multiply(np.multiply(rkorr, (vst-vsi)), nlkorr), np.squeeze(umat[0]))

x = np.array(unumpy.nominal_values(q))/1.602176634e-19
y = np.array(unumpy.nominal_values(rkorr))*1e6
xl = x.tolist()[0]
yl = y.tolist()[0]
xe = np.array(unumpy.std_devs(q))/1.602176634e-19
ye = np.array(unumpy.std_devs(rkorr))*1e6
xel = xe.tolist()[0]
yel = ye.tolist()[0]


#Plot



Y_LABEL = r"Radius $r$ in $\mu m$"
X_LABEL = r"Ladung in $e$"

X_MAJOR_TICK = 1
SAVE_AS = "./ELE/millikan.pdf"
#plot figure
fig, ax = plt.subplots()
ax.plot(xl[0:tommys_daten], yl[0:tommys_daten], "x", label="Messwerte")
ax.plot(xl[tommys_daten:], yl[tommys_daten:], "o", label="Messwerte")

ax.scatter(xl, yl, xerr=xel, yerr=yel)
ax.set_xlabel(X_LABEL)
ax.set_ylabel(Y_LABEL)
ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
ax.grid()
plt.savefig(SAVE_AS)
plt.show()
plt.close()

