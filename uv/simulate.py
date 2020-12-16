import tensorflow as tf
import scipy.misc
import model
import cv2
from subprocess import call
import time
import csv
import numpy as np
import config as cfg

sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, "save/model.ckpt")


xs = []
ys = []

with open(cfg.outputDir+cfg.currentDir+'/data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        #print(row[0], row[1])
        xs.append(row[0])
        ys.append(row[1])

print(xs[0])

i = 0
correct_num = 0
while(cv2.waitKey(10) != ord('q')):
    full_image = scipy.misc.imread('data/' + cfg.currentDir + '/' + xs[i] , mode="RGB")
    image = scipy.misc.imresize(full_image[cfg.modelheight:], [66, 200]) / 255.0
    
    image1 = scipy.misc.imresize(full_image[cfg.modelheight:], [66*3, 200*3])
    
    degrees = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})
    ###print("Label y: " + ys[i], 'prediced value:', np.argmax(degrees, axis=1),degrees)
    print("Label y: " + ys[i], 'prediced value:', np.argmax(degrees, axis=1))
    cv2.imshow("Feed", cv2.cvtColor(image1, cv2.COLOR_RGB2BGR))
    cv2.imshow("Original", cv2.cvtColor(full_image, cv2.COLOR_RGB2BGR))


    if int(ys[i]) == np.argmax(degrees, axis=1):
        correct_num += 1

    i += 1
    print('i:', i, 'correct_num: ', correct_num, 'percentage: ', correct_num/(i) * 100)
    

cv2.destroyAllWindows()