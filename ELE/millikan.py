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
#Abstand: 0.5e-3/(2*sqrt(3))

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

r0 = (3/2)*unumpy.sqrt((nl*(np.abs(vst - vsi))/drho/9.8072914)) #https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjrtI2vstv5AhVfQvEDHUCBChMQFnoECAQQAQ&url=https%3A%2F%2Fwww.uni-kassel.de%2Ffb10%2Findex.php%3FeID%3DdumpFile%26t%3Df%26f%3D2720%26token%3Dd35b3b1bc0149f09f203a8d91bdbf963e8108572&usg=AOvVaw0pgyv1jNUF-dF_znxzshgh


#Nach skript:
A = 1.257
lam = ufloat(72, 2)*1e-9

rkorr = np.squeeze(unumpy.sqrt(np.multiply(r0,r0) + A**2*lam**2/4) - A*lam/2)
#print(rkorr)
nlkorr = nl/(1 + A*lam/r0)

d = ufloat(0.006, 0.00005)

q = 3*np.pi*d*np.divide(np.multiply(np.multiply(rkorr, (vst + vsi)), nlkorr), np.squeeze(umat[0]))

x = np.array(unumpy.nominal_values(q))/1.602176634e-19
y = np.array(unumpy.nominal_values(rkorr))*1e6
xl = x.tolist()[0]
yl = y.tolist()[0]
xe = np.array(unumpy.std_devs(q))/1.602176634e-19
ye = np.array(unumpy.std_devs(rkorr))*1e6
xel = xe.tolist()[0]
yel = ye.tolist()[0]

#print(data[0], r0[0], rkorr[0], nlkorr[0], q[0], x[0], y[0], xel[0], yel[0])
#Plot



Y_LABEL = r"Radius $r$ in $\mu m$"
X_LABEL = r"Ladung in $e$"

X_MAJOR_TICK = 1
SAVE_AS = "./ELE/millikan.pdf"
#plot figure
fig, ax = plt.subplots()
# ax.plot(xl[0:tommys_daten], yl[0:tommys_daten], "x", label="Messwerte")
# ax.plot(xl[0:tommys_daten], yl[0:tommys_daten], "x", label="Messwerte")
# ax.plot(xl[tommys_daten:], yl[tommys_daten:], "o", label="Messwerte")

ax.errorbar(xl[0:unsere_daten], yl[0:unsere_daten], xerr=xel[0:unsere_daten], yerr=yel[0:unsere_daten], fmt="none", ecolor="red", label="Eigene Messwerte")
ax.errorbar(xl[unsere_daten:tommys_daten], yl[unsere_daten:tommys_daten], xerr=xel[unsere_daten:tommys_daten], yerr=yel[unsere_daten:tommys_daten], fmt="none", ecolor="blue", label="Tommys Messwerte")
ax.errorbar(xl[tommys_daten:], yl[tommys_daten:], xerr=xel[tommys_daten:], yerr=yel[tommys_daten:], fmt="none", ecolor="green", label="Sass Messwerte")
ax.set_xlabel(X_LABEL)
ax.set_ylabel(Y_LABEL)
ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
ax.grid()
ax.legend()
plt.savefig(SAVE_AS)
plt.show()
plt.close()


def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
X_START =0
Y_START =0
X_END = 9.3
Y_END = 9.3

X_MAJOR_TICK = 1
Y_MAJOR_TICK = 1
X_MINOR_TICK = X_MAJOR_TICK /5

#TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Anzahl der Elektronen"
X_LABEL = r"Ladung in $e$"

SAVE_AS = "./ELE/Ladungsverteilung.pdf"


arr = []
arrx = []

#print(xl)
peak_charge = 0.6902
singCh = [[],[]]
for i in range(1000):
    arrx.append(0.01*i)
    count =0 
    for J,j in enumerate(xl):
        if j*-1 > i *0.01 and j*-1 < (i+1) *0.01:
            count+=1
        if j*-1 > peak_charge*0.5 and j*-1 < peak_charge*1.5:
            singCh[0].append(j)
            singCh[1].append(xel[J])
    arr.append(count)
e = ufloat(gewichteterMittelwert(singCh[0],singCh[1]),intExtFehler(singCh[0],singCh[1]))*1.602176634e-19
    


#print(arr)
fig, ax = plt.subplots()
ax.set_xlim(X_START,X_END)
ax.set_ylim(Y_START,Y_END)
ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)
ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))

ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))


ax.plot(arrx,np.array(smooth(smooth(arr,50),50))*10)


arr =[]
arrx = []
for i in range(100):
    arrx.append(0.1*i)
    count =0 
    for J,j in enumerate(xl):
        if j*-1 > i *0.1 and j*-1 < (i+1) *0.1:
            count+=1
    arr.append(count)

ax.bar(arrx,arr,0.1,color = "orange", alpha = 0.7 )
ax.legend(["Ladungsverteilung geglättet","Ladungsverteilung"])
ax.grid()

plt.savefig(SAVE_AS)
plt.show()

em = ufloat(1.8128751720384433, 0.13490253869421437)*1e11
print(e)
print(em)
m = e/em
print(m)
print(round_err(float(unumpy.nominal_values(m*1e31)) ,float(unumpy.std_devs(m*1e31))))




        

