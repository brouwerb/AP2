from math import *
from tkinter.tix import X_REGION
import xlrd
import numpy as np
import string
from uncertainties import unumpy
from uncertainties import ufloat,nominal_value,std_dev

def getData(path):
    content=""
    with open (path)as f:
        content = f.read().replace(",",".")
        
    buf = content.split("\n")
    content=[]
    for i,I in enumerate(buf):
        if(i!=0 and i!=len(buf)-1):
            buffer=I.split("\t")
            buffer2=[]
            for N in buffer:
                
                buffer2.append(float(N))
            content.append(buffer2)
    return content

def round_err(num, err,  sig=2):
    posof1digit = floor(log10(abs(err)))
    rnum = round(num, sig-int(floor(log10(abs(err))))-1)
    srnum = str(rnum)
    if posof1digit <= 0:
        abrerr = err*10**(-int(floor(log10(abs(err))))+1)
        while len(srnum.split('.')[1]) <= -posof1digit:
            srnum += '0'
    
    else:
        abrerr = round(err, sig-int(floor(log10(abs(err))))-1)
        srnum = str(int(rnum))
    

    return(srnum + '(' + str(ceil(abrerr)) + ')')

def Alind(String):
    return [string.ascii_uppercase.index(String[0]),int(String[1:])-1]

def getAxisFromCell(Cell1,Cell2,path,sheet,plusCol=0):
    row1=Alind(Cell1)[1]
    collumn1 = Alind(Cell1)[0]+plusCol
    row2 = Alind(Cell2)[1]
    data = []
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(sheet)
    for i in range(row1,row2):
        data.append(worksheet.cell(i, collumn1).value)    
    return data
    
def getAxisEasy(startRow,Collumn,path,sheet,plusCol=0):

    data = []
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(sheet)
    i = startRow
    
    while worksheet.cell(i, Collumn).value != "":
        data.append(worksheet.cell(i, Collumn).value)  
        i+=1  
        try:
            worksheet.cell(i, Collumn).value
        except:
            break

    return data


def arrToUnumpy(arr,uncertantie):
    narr = []
    if isinstance(uncertantie,int) or isinstance(uncertantie,float) :
        for i in arr:
            narr.append(unumpy.uarray(i,uncertantie))
    else:
        for i in range(len(arr)):
            narr.append(unumpy.uarray(arr[i],uncertantie[i]))
    return narr

def arrToUnumpyf(arr,uncertantie):
    narr = []
    if isinstance(uncertantie,int) or isinstance(uncertantie,float) :
        for i in arr:
            narr.append(ufloat(i,uncertantie))
    else:
        for i in range(len(arr)):
            narr.append(ufloat(arr[i],uncertantie[i]))
    return narr


def getAxis(row1,collumn1,row2,path,sheet):
    data = []
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(sheet)
    for i in range(row1,row2):
        data.append(worksheet.cell(i, collumn1).value)    
    return data

def getRow(collumn1,row1,collumn2,path,sheet):
    data = []
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(sheet)
    for i in range(collumn1,collumn2):
        data.append(worksheet.cell(row1, i).value)    
    return data

def analogErr(a):
    return a/(2*np.sqrt(6))

def digitalErr(a):
    return a/(2*np.sqrt(3))
def uarrayToString(arr):
    buf = [] 
    for i in range(len(arr)):
        
        buf.append(round_errtex(float(unumpy.nominal_values(arr[i])),float(unumpy.std_devs(arr[i]))))
        
        #buf.append("scheiß Zehnerpotenzen")

    return buf


def FehlerFort(part1,part2,err1,err2,vals):
    return np.sqrt(part1(vals)**2*err1**2+part2(vals)**2*err2**2)

def arrToString(arr):
    string="["
    for i,I in enumerate(arr):
        if i !=len(arr)-1:
            string+=str(I)+","
        else:
            string+=str(I) +"]"
    return string


def genDataFromFunktion(amount,von,bis,params,func):
    x=[]
    y=[]
    
    for i in range(amount+1):
        x.append(von+i*(bis-von)/amount)
    for i in range(amount+1):
        
            
        y.append(func(x[i],params))
        
        #y.append(func(x[i]))

    return x,y



def getPlotable(rData):
    data=[[],[]]
    for i,I in enumerate(rData):
        data[0].append(I[0])
        data[1].append(I[1])
    return data

def getDataVonBis(path,von,bis):
    content=""
    with open (path)as f:
        content = f.read().replace(",",".")
        
    buf = content.split("\n")
    content=[]
    for i,I in enumerate(buf):
        if(von<=i and i<bis):
            buffer=I.split("\t")
            buffer2=[]
            for N in buffer:
                
                buffer2.append(float(N))
            content.append(buffer2)
    return content


def mirrorDataAroundX(x_val,x,y,verschiebungX =0):
    x = [i-x_val for i in x]
    x_n = []
    y_n = []
    for i in range(len(x)):
        if x[i]>0:
            x_n.append(x[i])
            x_n.append(-x[i])
            y_n.append(y[i])
            y_n.append(y[i])
    x_n = [i + verschiebungX for i in x_n]
    return x_n , y_n
        
def cutArrayByValue(arr, value , arr2 =[]):
    arr1_n =[]
    arr2_n =[]
    for i in range(len(arr)):
        print(arr[i])
        if arr[i]<=value:
            arr1_n.append(arr[i])
            if arr2 != []:
                arr2_n.append(arr2[i])
    return arr1_n,arr2_n




def wichtungsFaktor(err):
    return 1/err**2
def gewichteterMittelwert(vals,errs):
    buf =0
    for i in range(len(vals)):
        buf+= vals[i]*wichtungsFaktor(errs[i])
    buf2 =0 
    for i in range(len(vals)):
        buf2+= wichtungsFaktor(errs[i])
    return buf/buf2
def internerFehler(errs):
    buf=0
    for i in range(len(errs)):
        buf+=wichtungsFaktor(errs[i])
    return np.sqrt(1/buf)
def externerFehler(vals,errs):
    buf1=0
    gewAvg = gewichteterMittelwert(vals,errs)
    for i in range(len(vals)):
        buf1+=wichtungsFaktor(errs[i])*(vals[i]-gewAvg)**2
    buf2 =0
    for i in range(len(vals)):
        buf2+= wichtungsFaktor(errs[i])
    return np.sqrt(buf1/((len(vals)-1)*buf2))
    
def intExtFehler(vals, errs):
    return max(internerFehler(errs),externerFehler(vals,errs))

def cut(xy):
    for i, I in enumerate(xy[1]):
        if xy[1][i] <= 0 and xy[1][i+1] >=0:
            ind = i
            break
    for i in range(ind):
        now = xy[1][i]
        if -100 < now < -70 and xy[1][i+1] >  -70:
            n = i
            break
    return(n)

def constructdata(udata):
    data = []
    for i, I in enumerate(udata):
        data.append([])
        for j in I:
            data[i].append(round_err(float(unumpy.nominal_values(j)), float(unumpy.std_devs(j))))
    return data


def printtableaslatex(data, name, header):
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\begin{tabular}{c" + "|c"*(len(data[0])-1) + "}")
    #print("\\hline")
    print("\\textbf{", end="")
    print( *header, sep ="} & \\textbf{", end="} \\\\ \n")
    print("\\hline")
    for i in range(len(data)):
        print(*data[i], sep=" & ", end="\\\\ \n",)
    # print("\\hline")
    print("\\end{tabular}")
    print("\\caption{"+name+"}")
    print("\\end{table}")

def savetableastxt(data, name, file, header):
    with open(file+".txt", "w") as f:
        f.write("\\begin{table}[H]\n")
        f.write("\\centering\n")
        f.write("\\begin{tabular}{c" + "|c"*(len(data[0])-1) + "}\n")
        
        f.write("\\textbf{" + "} & \\textbf{".join(header) + "} \\\\ \n")
        f.write("\\hline\n")
        for i in range(len(data)):
            f.write(" & ".join(data[i]) + "\\\\ \n")
        # f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\caption{"+name+"}\n")
        f.write("\\label{tab:"+file+"}\n")
        f.write("\\end{table}\n")

def round_errtex(num, err,  sig=2):
    posof1digit = floor(log10(abs(err)))
    magnum = floor(log10(abs(num)))
    rnum = round(num, sig-int(floor(log10(abs(err))))-1)
    srnum = str(rnum)
    if posof1digit < -3:
        abrerr = err*10**(sig-int(floor(log10(abs(err))))-1)
        tnum = round(num*10**-magnum, sig)
        return("$" + str(tnum) + '(' + str(ceil(abrerr)) + ')' + " \\cdot 10^{" + str(magnum) + "}" + "$")

        
    elif posof1digit <= 0:
        abrerr = err*10**(sig-int(floor(log10(abs(err))))-1)
        while len(srnum.split('.')[1]) <= -posof1digit:
            srnum += '0'
        return(srnum + '(' + str(int(ceil(abrerr))) + ')')
    
    else:
        abrerr = round(err, sig-int(floor(log10(abs(err))))-1)
        srnum = str(int(rnum))
    

        return(srnum + '(' + str(ceil(abrerr)) + ')')
def exponentialNum(num,sig=2):
    magnum = floor(log10(abs(num)))
    tnum = round(num*10**-magnum, sig)
    return("$" + str(tnum) + " \\cdot 10^{" + str(magnum) + "}" + "$")

def round_errtexU(num):
    return round_errtex(nominal_value(num),std_dev(num))

def genIntBounds(a,inter):
    return [[i-inter for i in a],[i + inter for i in a ]]

