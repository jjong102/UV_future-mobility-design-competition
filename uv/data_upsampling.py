import random
import csv
import numpy as np
import config as cfg

x1 = []
#y1 = []
x2 = []
x3 = []
x4 = []
#y3 = []
#upsample = []
max_val = 0

#read data.csv
with open('data/' + cfg.currentDir + '/data.csv', newline='') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        #print(row[0], row[1])
        if int(row[1]) == 1:
            x1.append(row)
        elif int(row[1]) == 2:
            x2.append(row)    
        elif int(row[1]) == 3:
            x3.append(row)
        elif int(row[1]) == 4:
            x4.append(row)

            


max_val = max(len(x1),len(x2),len(x3),len(x4))
#print(len(x1),len(x2),len(x3))
#print(max_val)

x1_add = []
x2_add = []
x3_add = []
x4_add = []


if( max_val - len(x1) > len(x1)):
    x1_add = random.sample(x1, len(x1))
else:
    x1_add = random.sample(x1, max_val - len(x1))

if( max_val - len(x2) > len(x2)):
    x2_add = random.sample(x2, len(x2))
else:
    x2_add = random.sample(x2, max_val - len(x2))

if( max_val - len(x3) > len(x3)):
    x3_add = random.sample(x3, len(x3))
else:
    x3_add = random.sample(x3, max_val - len(x3))

if( max_val - len(x4) > len(x4)):
    x4_add = random.sample(x4, len(x4))
else:
    x4_add = random.sample(x4, max_val - len(x4))



#print(len(x2_add))


with open('data/' + cfg.currentDir + '/data.csv', 'a') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|')
    filewriter.writerows(x1_add)
    filewriter.writerows(x2_add)
    filewriter.writerows(x3_add)
    filewriter.writerows(x4_add)
    


