from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from AP import *
sys.path.pop(0)
from uncertainties.unumpy  import uarray, nominal_values,std_devs
import math

B_Feld_I = uarray(1.3,1.3*0.025+0.1)


col = ["A","D","G"]
radien =  [uarray(0.03,0.0005),uarray(0.04,0.0005),uarray(0.05,0.005)]

def calHelmholtzB (I):
    Helm_R = uarray(0.15,0.002)
    N = 130
    mu0 = 1.256637e-6
    return mu0 * math.pow(4/5,3/2) * N * I / Helm_R
def eDruchm(B,r,Ubesch):
    return (2*Ubesch/(B**2*r**2))


gewMitt = []
em = [[],[]]
for i in range (3):
    arr = getAxisFromCell(col[i]+"13",col[i]+"22","./ELE/data.xls","Faden")
    
    uarr= []
    for j in range(len (arr)):
        uarr.append(arr[j]*0.08+8)
    gewMitt.append(uarray(gewichteterMittelwert(arr,uarr),intExtFehler(arr,uarr)))
    em_buf =eDruchm(calHelmholtzB(B_Feld_I),radien[i],gewMitt[i])
    print(round_err(float(nominal_values(em_buf))*1e-11,float(std_devs(em_buf))*1e-11))
    em[0].append(float(nominal_values(em_buf)))
    em[1].append(float(std_devs(em_buf)))

col = ["B","D","G"]

gewMitt = []

for i in range (3):
    arr = getAxisFromCell(col[i]+"29",col[i]+"39","./ELE/data.xls","Faden")
    uarr= []
    for j in range(len (arr)):
        uarr.append(arr[j]*0.025+0.1)
    gewMitt.append(uarray(gewichteterMittelwert(arr,uarr),intExtFehler(arr,uarr)))
    em_buf =eDruchm(calHelmholtzB(gewMitt[i]),radien[i],uarray(150,150*0.08+8))
    print(round_err(float(nominal_values(em_buf)*1e-11),float(std_devs(em_buf))*1e-11))
    em[0].append(float(nominal_values(em_buf)))
    em[1].append(float(std_devs(em_buf)))


print("final result mal 10^-11")
print(round_err(gewichteterMittelwert(em[0],em[1])*1e-11,intExtFehler(em[0],em[1])*1e-11))

    








