#airun.py

#import xhat as hw
import time
import cv2
import config as cfg
#import opidistance3 as dc
import tensorflow as tf
import scipy.misc
import numpy as np
import model
from jetbot import Robot

import os
import sys
import signal
import csv

def gstreamer_pipeline(
    capture_width=320,
    capture_height=240,
    display_width=320,
    display_height=240,
    framerate=15,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

st = 0

if __name__ == '__main__':
    
    sess = tf.InteractiveSession()
    saver = tf.train.Saver()
    saver.restore(sess, "save/model.ckpt")

    start_flag = False

    #testing speed variation
    speed_change_flag = False

    if speed_change_flag:
        cfg.maxturn_speed = cfg.ai_maxturn_speed
        cfg.minturn_speed = cfg.ai_minturn_speed
        cfg.normal_speed_left = cfg.ai_normal_speed_left
        cfg.normal_speed_right = cfg.ai_normal_speed_right
    
   #c = cv2.VideoCapture(0)
   #c.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
   #c.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
   #c.set(cv2.CAP_PROP_FPS, 15)
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    robot = Robot()
    count = 0

    while(True):
        _,full_image = cap.read()
        #full_image = cv2.resize(full_image, (320,240))
        image = scipy.misc.imresize(full_image[cfg.modelheight:], [66, 200]) / 255.0
        image1 = scipy.misc.imresize(full_image[cfg.modelheight:], [66*2, 200*2])

        cv2.imshow('original',full_image)
        #cv2.imshow("view of AI", cv2.cvtColor(image1, cv2.COLOR_RGB2BGR))
        cv2.imshow("view of AI", image1)

        
        wheel = model.y.eval(session=sess,feed_dict={model.x: [image], model.keep_prob: 1.0})
        cfg.wheel = np.argmax(wheel, axis=1)
        #print('wheel value:', cfg.wheel, wheel)
        print('wheel value:', cfg.wheel, model.softmax(wheel))

    
        k = cv2.waitKey(5)
        if k == ord('q'):  #'q' key to stop program
            break

        """ Toggle Start/Stop motor movement """
        if k == ord('a'): 
            if start_flag == False: 
                start_flag = True
            else:
                start_flag = False
            print('start flag:',start_flag)
   
        #to avoid collision when ultrasonic sensor is available
        #length = 30 #dc.get_distance()
        #if  5 < length and length < 15 and start_flag:
        #    hw.motor_one_speed(0)
        #    hw.motor_two_speed(0)
        #    print('Stop to avoid collision')
        #    time.sleep(0.5)
        #    continue
        
        
        if start_flag:
           
            if cfg.wheel == 0:
                robot.stop()

            elif cfg.wheel == 1:   #left turn
                robot.left(speed=0.28)
                st += 1
                
            elif cfg.wheel == 2:   #Go straight
                robot.forward(speed=0.4)
                st += 1
                count = count - 1
            elif cfg.wheel == 3:   #right turn
                robot.right(speed=0.28)
                st += 1
                
            elif cfg.wheel == 4:
                if count < 0:
                    count = 0
                    robot.stop()
                    time.sleep(3)
                    robot.forward(speed=0.35)
                    time.sleep(0.7)
                else:
                    robot.stop()
                       
            
            if st % 3 == 0:       # stablity
                print(st)
                robot.stop()

        else:
            robot.stop()
           
            # hw.motor_one_speed(0)
           # hw.motor_two_speed(0)
           # cfg.wheel = 0

        
#hw.motor_clean()
cv2.destroyAllWindows()
