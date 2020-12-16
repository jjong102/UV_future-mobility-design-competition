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

# img = cv2.imread('steering_wheel_image.jpg',0)
# rows,cols = img.shape

smoothed_angle = 0

xs = []
ys = []

with open(cfg.outputDir+cfg.currentDir+'/data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        #print(row[0], row[1])
        xs.append(row[0])
        ys.append(row[1])

print(len(ys))
total_num = len(ys)

i = 0
correct_num = 0
left_num = 0
forward_num = 0
right_num = 0
correct_left = 0
correct_right = 0
correct_forward = 0

while(True):
    full_image = scipy.misc.imread('data/' + cfg.currentDir + '/' + xs[i] , mode="RGB")
    image = scipy.misc.imresize(full_image[cfg.modelheight:], [66, 200]) / 255.0
    
    degrees = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})

    if int(ys[i]) == np.argmax(degrees, axis=1):
        correct_num += 1

    if int(ys[i]) == 1:
        left_num += 1
        if int(ys[i]) == np.argmax(degrees, axis=1):
            correct_left += 1

    if int(ys[i]) == 2:
        forward_num += 1
        if int(ys[i]) == np.argmax(degrees, axis=1):
            correct_forward += 1

    if int(ys[i]) == 3:
        right_num += 1
        if int(ys[i]) == np.argmax(degrees, axis=1):
            correct_right += 1



    i += 1

    if total_num == i:
        break

print('i:', i, 'correct_num: ', correct_num, 'percentage: ', correct_num/(i) * 100)
    
    
if left_num != 0:
    print('left_num: ', left_num, 'correct_left: ', correct_left, 'percentage: %0.1f' % (correct_left/left_num*100) )

if forward_num != 0:
    print('forward_num: ', forward_num, 'correct_forward: ', correct_forward, 'percentage: %0.1f' % (correct_forward/forward_num*100) )

if right_num != 0:
    print('right_num: ', right_num, 'correct_right: ', correct_right, 'percentage: %0.1f' % (correct_right/right_num*100) )

