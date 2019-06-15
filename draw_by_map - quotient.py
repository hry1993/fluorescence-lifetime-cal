import csv
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


minR = 0.75 # min R, less than this will not be shown in image, range from 0 to 1
left = 0 # below this will be shown as purple
right = 2 # above this will be shown as red, right should larger than left

img = []
result = []
size = 1024

countL = 0
distance = 0.2
countN = 9
count = []
countV = []
number = 0
for i in range(countN):
    count.append(countL + distance * (i + 1))
    countV.append(0)
print(count)

# initial result sets
csvfile = open('resultD.csv')
readCSV = csv.reader(csvfile, delimiter=',')
for row in readCSV:
    resultRow = []
    for i in range(len(row)):
        temp = re.split(',|\[|\]',row[i])
        temp[2] = temp[2].strip()
        if (float(temp[2]) < minR or float(temp[1]) == 0):
            temp[1] = np.nan
        elif (float(temp[1]) > right):
            temp[1] = right
        elif (float(temp[1]) < left):
            temp[1] = right
        if (np.isnan(float(temp[1]))):
            pass
        else:
            number += 1
            if (float(temp[1]) <= countL):
                countV[0] += 1
            for j in range(countN):
                if ((count[j] - distance) < float(temp[1]) <= (count[j])):
                    countV[j] += 1
            if (float(temp[1]) > (countL + distance * countN)):
                countV[countN - 1] += 1
        resultRow.append(float(temp[1]))
    result.append(resultRow)
csvfile.close()

check = 0
for i in range(countN):
    check += countV[i]
if (check == number):
    print("right")
else:
    print(check)
    print(number)

csvFile = open('count.csv', 'w', newline='')
writer = csv.writer(csvFile)


for i in range(countN):
    writer.writerow([str(countL + distance * i) + "-" + str(countL + distance * (i + 1)), countV[i]])

fig, ax = plt.subplots()
cax = ax.imshow(result, interpolation='nearest', cmap=cm.rainbow)
cbar =fig.colorbar(cax, ticks=[left, right])

plt.show()
