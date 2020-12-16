import scipy.misc
import cv2
import random
import csv
#from mlxtend.preprocessing import one_hot
import numpy as np
import config as cfg


#delete dc_img* in data.csv file
originalrows = []
with open('data/' + cfg.currentDir + '/data.csv', newline='') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        #print(row[0], row[1])
        if row[0][:2] != 'dc':
            originalrows.append(row)

with open('data/' + cfg.currentDir + '/data.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|')
    filewriter.writerows(originalrows)


x1 = []
#y1 = []
x2 = []
x3 = []
#y3 = []


#read data.csv
with open('data/' + cfg.currentDir + '/data.csv', newline='') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in filereader:
        #print(row[0], row[1])
        if int(row[1]) == 1:
            x1.append(row[0])
        elif int(row[1]) == 2:
            x2.append(row[0])    
        elif int(row[1]) == 3:
            x3.append(row[0])

cfg.f=open(cfg.outputDir+cfg.currentDir+'/data.csv','a')
cfg.fwriter = csv.writer(cfg.f)

for i in range(len(x1)):
    full_image = cv2.imread('data/' + cfg.currentDir + '/' + x1[i] , cv2.IMREAD_COLOR)
    full_image = cv2.flip(full_image, 1)
    myfile = 'data/' + cfg.currentDir + '/dc_' + x1[i]
    cv2.imwrite(myfile,full_image)
    cfg.fwriter.writerow(('dc_' + x1[i], 3))

for i in range(len(x3)):
    full_image = cv2.imread('data/' + cfg.currentDir + '/' + x3[i] , cv2.IMREAD_COLOR)
    full_image = cv2.flip(full_image, 1)
    myfile = 'data/' + cfg.currentDir + '/dc_' + x3[i]
    cv2.imwrite(myfile,full_image)
    cfg.fwriter.writerow(('dc_' + x3[i], 1))

for i in range(len(x2)):
    full_image = cv2.imread('data/' + cfg.currentDir + '/' + x2[i] , cv2.IMREAD_COLOR)
    full_image = cv2.flip(full_image, 1)
    myfile = 'data/' + cfg.currentDir + '/dc_' + x2[i]
    cv2.imwrite(myfile,full_image)
    cfg.fwriter.writerow(('dc_' + x2[i], 2))


