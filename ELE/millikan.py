from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties import unumpy , ufloat
import matplotlib.pyplot as plt

#Unsere Daten
col = ["A","B","C"]
data = []
for i in range(8, 33):
    data.append(getRow(0,i,3, "./ELE/data.xls","Millikan") + [0.5*(7.57-3.72)*1e-3])

#tommys Daten
for i in range(5, 26):
    row = getRow(0,i,3, "./ELE/tommy.xls","Tabelle1")
    data.append([row[2], row[1], row[0], 0.5*(3.55)*1e-3])


#import data from txt file
with open("./ELE/datamoodle.txt") as f:
    for line in f:
        row = line.split()
        data.append([float(row[1].replace(",",".")),float(row[3].replace(",",".")),float(row[2].replace(",",".")), float(row[0].replace(",","."))])


#Unsicherheiten:
#Spannung: 1/(2*sqrt(3))
#Zeit: Ablese sprt((0.1/(2*sqrt(3)))**2 + 0.4) Reaktions 0.2
#Abstand: 0.5*10e-3/(2*sqrt(3))

print(data)

udata = unumpy.umatrix(data, [[1/(2*sqrt(3)), sqrt((0.1/(2*sqrt(3)))**2 + 0.4), sqrt((0.1/(2*sqrt(3)))**2 + 0.4), 0.5e-3/(2*sqrt(3))]])

umat = udata.transpose()

# Viskosität Luft http://www.peacesoftware.de/einigewerte/luft.html bei 1 bar und 24°C: 18.4304*10e-6
nl = 18.4304*10**-6
#Dichte Öl = 871 kg/m³
#Dichte Luft = 1.17228 kg/m³ http://www.peacesoftware.de/einigewerte/luft.html

drho = 871 - 1.17228

# s = vt  v = s/t
vst = np.squeeze(umat[3]/umat[1])
vsi = np.squeeze(umat[3]/umat[2])

r0 = (3/2)*unumpy.sqrt((nl*(vst + vsi)/drho*9.8072914)) #https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjrtI2vstv5AhVfQvEDHUCBChMQFnoECAQQAQ&url=https%3A%2F%2Fwww.uni-kassel.de%2Ffb10%2Findex.php%3FeID%3DdumpFile%26t%3Df%26f%3D2720%26token%3Dd35b3b1bc0149f09f203a8d91bdbf963e8108572&usg=AOvVaw0pgyv1jNUF-dF_znxzshgh

#Nach skript:
A = 1.257
lam = ufloat(72, 2)*1**-9

rkorr = np.squeeze(unumpy.sqrt(r0 + A**2*lam**2/4) - A*lam/2)

nlkorr = nl/(1 + A*lam/r0)

d = ufloat(0.006, 0.00005)

print(r0, rkorr)

q = 3*np.pi*d*np.divide(np.multiply(np.multiply(rkorr, (vst-vsi)), nlkorr), np.squeeze(umat[0]))

x = np.array(unumpy.nominal_values(q))/1.602176634e-19
y = np.array(unumpy.nominal_values(rkorr))
print(x, y)

plt.scatter(x, y)
plt.show()