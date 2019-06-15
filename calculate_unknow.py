import csv
import glob
import numpy as np
from scipy.optimize import curve_fit

sets = []  # record of all data
files = glob.glob('*.asc')  # file names
z = len(files)  # number of files (auto)
t = 0.48 # total time (ms) changeable
minR = 0.75 # min R, less than this will not be shown in image, range from 0 to 1
t = 1000 * t / (z - 1)
print(t)
pointCollectionRate = 1.1 # delete points less than average I * rate

positions = []  # positions need to be counted, background subtraction start
firstSet = []
print(files)
lines = open(files[0]).readlines()
size = len(str.split(lines[0])) - 1
print(size)
for line in lines:
    temp = str.split(line)
    temp.pop(0)
    firstSet.append(temp)
sum = 0
sumL = 0
ave = firstSet[0][0]
aveCount = 0
aveCountL = 0
for i in range(len(firstSet)):
    for l in range(len(firstSet[0])):
        if (float(ave) * pointCollectionRate >= float(firstSet[i][l])):
            # change value before >= to delete points, like 650
            sum = sum + float(firstSet[i][l])
            aveCount = aveCount + 1
            ave = sum / aveCount
        else:
            sumL = sumL + float(firstSet[i][l])
            aveCountL = aveCountL + 1
            positions.append([i, l])
aveL = sumL/aveCountL
print(ave,aveL)
print(positions)
# reduce points

for fileName in files:
    lines = open(fileName).readlines()
    data = []
    for line in lines:
        temp = str.split(line)
        temp.pop(0)
        data.append(temp)
    sets.append(data)
result = []
resultD = []
tValue = []
rValue = []
allV = []
a1V = []
bV = []
dV = []
l1V = []
a2V = []
l2V = []
a12V = []

for i in range(size):
    resultRow = []
    resultDRow = []
    tRow = []
    rRow = []
    allRow = []
    a1Row = []
    bRow = []
    dRow = []
    l1Row = []
    a2Row = []
    l2Row = []
    a12Row = []
    for l in range(size):
        resultRow.append([0, 0])
        resultDRow.append([0, 0])
        allRow.append([0,0,0,0,0,0,0,0,0])
        tRow.append(0)
        rRow.append(0)
        a1Row.append(0)
        bRow.append(0)
        dRow.append(0)
        l1Row.append(0)
        a2Row.append(0)
        l2Row.append(0)
        a12Row.append(0)
    result.append(resultRow)
    resultD.append(resultDRow)
    tValue.append(tRow)
    rValue.append(rRow)
    a1V.append(a1Row)
    bV.append(bRow)
    dV.append(dRow)
    l1V.append(l1Row)
    a2V.append(a2Row)
    l2V.append(l2Row)
    a12V.append(a12Row)
    allV.append(allRow)
# initial result sets

x = []
for i in range(z):
    x.append(i)
# x = [1,2,3,4,5...] change time here

def func(x, a1, b, d, l1, a2, l2):
    return a1 * np.exp(-(d + t * x)/ l1) + a2 * np.exp(-(d + t * x)/ l2) + b


csvFile = open('result.csv', 'w', newline='')
writer = csv.writer(csvFile)
csvFileD = open('resultD.csv', 'w', newline='')
writerD = csv.writer(csvFileD)
tcsvFile = open('t.csv', 'w', newline='')
twriter = csv.writer(tcsvFile)
rcsvFile = open('r.csv', 'w', newline='')
rwriter = csv.writer(rcsvFile)
a1csvFile = open('a1.csv', 'w', newline='')
a1writer = csv.writer(a1csvFile)
a2csvFile = open('a2.csv', 'w', newline='')
a2writer = csv.writer(a2csvFile)
a12csvFile = open('a12.csv', 'w', newline='')
a12writer = csv.writer(a12csvFile)
bcsvFile = open('b.csv', 'w', newline='')
bwriter = csv.writer(bcsvFile)
dcsvFile = open('d.csv', 'w', newline='')
dwriter = csv.writer(dcsvFile)
l1csvFile = open('l1.csv', 'w', newline='')
l1writer = csv.writer(l1csvFile)
l2csvFile = open('l2.csv', 'w', newline='')
l2writer = csv.writer(l2csvFile)
allcsvFile = open('all.csv', 'w', newline='')
allwriter = csv.writer(allcsvFile)

for i in range(len(positions)):
    l = positions[i][0]
    m = positions[i][1]
    y = []
    for j in range(z):
        y.append(float(sets[j][l][m]))
    try:
        popt, pcov = curve_fit(func, x, y)
        allV[l][m][0] = popt[0]
        allV[l][m][1] = popt[1]
        allV[l][m][2] = popt[2]
        allV[l][m][3] = popt[3]
        allV[l][m][4] = popt[4]
        allV[l][m][5] = popt[5]
        a1V[l][m] = popt[0]
        a2V[l][m] = popt[4]
        l1V[l][m] = popt[3]
        l2V[l][m] = popt[5]
        bV[l][m] = popt[1]
        dV[l][m] = popt[2]
        result[l][m][0] = (popt[0] * popt[3] * popt[3] + popt[4] * popt[5] * popt[5]) / (popt[0] * popt[3] + popt[4] * popt[5])
        tValue[l][m] = result[l][m][0]
        allV[l][m][6] = tValue[l][m]
        a12V[l][m] = popt[0]/popt[4]
        resultD[l][m][0] = a12V[l][m]
        allV[l][m][7] = a12V[l][m]
        residuals = []
        ss_res = 0
        for k in range(z):
            residuals = y[k] - func(x[k], popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
            ss_res = ss_res + residuals ** 2
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        result[l][m][1] = 1 - (ss_res / ss_tot)
        resultD[l][m][1] = result[l][m][1]
        rValue[l][m] = result[l][m][1]
        allV[l][m][8] = rValue[l][m]
        print(result[l][m])
    except:
        pass

for i in range(size):
    writer.writerow(result[i])
    writerD.writerow(resultD[i])
    twriter.writerow(tValue[i])
    rwriter.writerow(rValue[i])
    a1writer.writerow(a1V[i])
    a2writer.writerow(a2V[i])
    l1writer.writerow(l1V[i])
    l2writer.writerow(l2V[i])
    allwriter.writerow(allV[i])
    a12writer.writerow(a12V[i])
    bwriter.writerow(bV[i])
    dwriter.writerow(dV[i])

csvFile.close()
csvFileD.close()
tcsvFile.close()
rcsvFile.close()
a1csvFile.close()
a2csvFile.close()
l1csvFile.close()
l2csvFile.close()
allcsvFile.close()
a12csvFile.close()
bcsvFile.close()
dcsvFile.close()

