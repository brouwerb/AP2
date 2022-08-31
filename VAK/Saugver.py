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
from scipy import optimize

def exp(x,a,b):
    return np.exp(x*a)*np.exp(b)

def arrExp(x,a):
    return(exp(x,a[0],a[1]))


time_err = 0.5
rawTimes = [getAxisEasy(4,i,"./VAK/Vak.xls","nr.3")  for i in range(0,5,2)]
rawI = [getAxisEasy(4,i,"./VAK/Vak.xls","nr.3")  for i in range(1,6,2)]
rawP = [[kalibrierungsFunktion(j)*1e2 for j in i] for i in rawI]
legende = ["Schlauch",r"Kapillare 3$mm$",r"Kapillare 2$mm$"]

print(rawTimes,rawP)
print([len(i) for i in rawTimes],[len(i) for i in rawP])

Y_LABEL = r"Druck $p$ in $Pa$"
X_LABEL = r"Zeit $t$ in $s$"
COLOR_STYLE = ["red","green","blue"]
SAVE_AS = "./VAK/Saugver.pdf"
fig, ax = plt.subplots()
ax.grid()
trenner = [[9,10],[10,14],[14,18]]
bounds = [[[[-np.inf,-np.inf],[-0.175,np.inf]],[[-np.inf,-np.inf],[np.inf,np.inf]]],
        [[[-np.inf,-np.inf],[np.inf,np.inf]],[[-0.00652137,-np.inf],[-0.00452137,np.inf]]],
        [[[-np.inf,-np.inf],[np.inf,np.inf]],[[-0.00552137,-np.inf],[-0.00252137,np.inf]]]]
steigung = []
for i in range(len(rawTimes)):
    ax.scatter(rawTimes[i],rawP[i],s=20,linewidths=1,edgecolors="black",zorder=10,color = COLOR_STYLE[i])
    ax.errorbar(rawTimes[i],rawP[i],fmt="none",xerr=time_err,ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8)

for i in range(len(rawTimes)):   
    vals, errs = optimize.curve_fit(exp,rawTimes[i][:trenner[i][0]],rawP[i][:trenner[i][0]],bounds = bounds[i][0])
    print(vals)
    steigung.append([vals.tolist(),[]])
    rdata = [round_errtex(vals[i], np.sqrt(np.diag(errs))[i]) for i in range(len(vals))]
    buf = genDataFromFunktion(100,0,rawTimes[i][trenner[i][0]],vals,arrExp)
    ax.plot(buf[0],buf[1],linestyle="--",color = COLOR_STYLE[i])
    vals, errs = optimize.curve_fit(exp,rawTimes[i][trenner[i][1]:],rawP[i][trenner[i][1]:],maxfev= 5000,bounds =bounds[i][1])
    steigung[i][1] = vals.tolist()
    buf = genDataFromFunktion(100,rawTimes[i][trenner[i][1]],rawTimes[i][-1],vals,arrExp)
    ax.plot(buf[0],buf[1],linestyle="dotted",color = COLOR_STYLE[i])

# print(steigung)
# Volumen = ufloat(3,0.1)
# steigung = [[ i[0]*Volumen*-1,np.log(i[1])] for i in steigung for j in i] 
# data = [["Schlauch","3mm","2mm"],[i[0][0] for i in steigung],[i[0][0] for i in steigung]]
# savetableastxt([*zip(*data)], "Theortische Werte", "./VAK/Steigungnen", ["Name","Steigung molekular","Steigung viskos"])

ax.set_xlabel(X_LABEL)
ax.set_ylabel(Y_LABEL)
ax.legend(legende)

plt.yscale("log")
plt.savefig(SAVE_AS)
plt.show()
