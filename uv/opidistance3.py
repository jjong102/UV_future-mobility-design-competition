from pyA20.gpio import gpio as GPIO
from pyA20.gpio import port
import time

GPIO.init()

Echo = port.PA13
Trig = port.PA14


GPIO.setcfg(Trig, GPIO.OUTPUT)
GPIO.setcfg(Echo, GPIO.INPUT)

GPIO.output(Trig, GPIO.LOW)

time.sleep(1)

def get_distance():
    GPIO.output(Trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trig, GPIO.LOW)

    while GPIO.input(Echo)==0:
        pass
    start = time.time()

    while GPIO.input(Echo)==1:
        pass
    end = time.time()

    elapsed = end - start

    distance_cm = elapsed * 34000
    distance_cm = distance_cm / 2

    #print( "Distance : %.1f" % distance_cm)
    return distance_cm


if __name__ == '__main__':

    while(True):
        cm = get_distance()
        print( "Distance : %.1f" % cm)
        time.sleep(0.1)








#GPIO.cleanup()



