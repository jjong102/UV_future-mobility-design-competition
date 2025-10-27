from jetbot import Robot
from jetbot import Camera, bgr8_to_jpeg
import ipywidgets
import traitlets
import PIL.Image
#import xhat as hw
import time
import cv2
import uv.UV_config as cfg

import os
import sys
import signal
import csv

def recording():
    if cfg.recording:
        cfg.recording = False
        cfg.f.close()
    else:
        cfg.recording = True
        if cfg.currentDir == '':
            cfg.currentDir = time.strftime('%Y-%m-%d')
            os.mkdir(cfg.outputDir+cfg.currentDir)
            cfg.f=open(cfg.outputDir+cfg.currentDir+'/data.csv','w')
        else:
            cfg.f=open(cfg.outputDir+cfg.currentDir+'/data.csv','a')
        cfg.fwriter = csv.writer(cfg.f)

def saveimage():
    if cfg.recording:
        myfile = 'img_'+time.strftime('%Y-%m-%d_%H-%M-%S')+'_'+str(cfg.cnt)+'.jpg'
        print(myfile, cfg.wheel)

        cfg.fwriter.writerow((myfile, cfg.wheel))

        cv2.imwrite(cfg.outputDir+cfg.currentDir+'/'+ myfile,full_image)

        cfg.cnt += 1

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


if __name__ == '__main__':
    
    #camera = Camera.instance(width=300, height=300)
    #image_widget = ipywidgets.Image()
    robot = Robot()
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    start_flag = False
    
  #  c = cv2.VideoCapture(0)
  #  c.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
  #  c.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    #c.set(cv2.CAP_PROP_FPS, 15)

    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            _,full_image = cap.read()
        
            cv2.imshow('frame',full_image)
    
            k = cv2.waitKey(5)
            if k == ord('q'):  #'q' key to stop program
                break

            """ Toggle Start/Stop motor movement """
            if k == 115: #115:'s'
                if start_flag == False: 
                    start_flag = True
                else:
                    start_flag = False
                print('start flag:',start_flag)

            """ Toggle Record On/Off  """
            if k == 114: #114:'r'
                recording()
                if cfg.recording:
                    start_flag = True
                else:
                    start_flag = False
                    cfg.cnt = 0
                print('cfg.recording:',cfg.recording)

        #save image files and images list file   
            if cfg.recording:
                saveimage()
                print(cfg.cnt)
        
            if start_flag:
                # Left arrow: 81, Right arrow: 83, Up arrow: 82, Down arrow: 84
                if k == 81: 
                    robot.left(speed=0.3)
                    #print('Straight')
                    cfg.wheel = 1
                
                   
                elif k == 83: 
                    robot.right(speed=0.3)
                
                    cfg.wheel = 3
                   
                elif k == 82: 
                    robot.forward(speed=0.35)
                
                    cfg.wheel = 2
                   
                elif k == 84:
                    
                    time.sleep(3)
                    robot.forward(speed=0.35)
                    time.sleep(1)
                    cfg.wheel = 4
                elif k==ord('p'):
                    cfg.wheel =4

                else:
                    robot.stop()
                    cfg.wheel=0
                                                          
            else:
	                   	            
                robot.stop()
                cfg.wheel = 0
                
        
#hw.motor_clean()
cv2.destroyAllWindows()
