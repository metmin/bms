from matplotlib.text import get_rotation
import serial
import pyvesc
from pyvesc.VESC.messages import GetValues, SetRPM, SetCurrent, SetRotorPositionMode, GetRotorPosition
import serial
import time
import datetime
import numpy as np
from time import sleep
import multiprocessing
import RPi.GPIO as GPIO
from os.path import exists
GPIO.setmode(GPIO.BCM)

GAIN = 1

RX = 23

dist = multiprocessing.Value("d", 0)
velocity = multiprocessing.Value("f", 0)

serialport = '/dev/ttyACM0'
values = multiprocessing.Array("f",range(4))

def get_rpm(counter = 1):
    try:
    
        f = open("rpm.txt", "r")
        data = f.read()
        f.close()
        return int(data)
    
    except:
        
        if counter >= 100:
            return -1
        
        sleep(0.1)
        return get_rpm(counter + 1)    

def control(counter = 1):
    if not (exists(serialport)):
        sleep(1)
        if(counter < 60):
            print('motor sürücüsünün bağlı olduğu port bulunamadı yeniden deneniyor')
            return control(counter + 1)
        return False        
    return True
    

def get_values_example(values):

    if control() == False:
        print('Motor sürücü kartı bulunamadı, program kapanıyor.')
        return
    old_time = time.time()
    new_time = time.time()
    old_distance = 0
    new_distance = 0
    with serial.Serial(serialport, baudrate=115200, timeout=0.05) as ser:
        try:
            while(True):
                count = 0
                time.sleep(3)

                while(True):
                    rpm = get_rpm()
                    if (rpm == -1):
                        return
                    
                    ser.write(pyvesc.encode_request(GetValues))
                    (response, consumed) = pyvesc.decode(ser.read(78))
                    new_time = time.time()
                    diff = int (new_time - old_time)
                    if diff >= 1:
                        print(f'rpm => {rpm}')
                        old_time = time.time()
                        try:
                            attrs = vars(response)
                            #print(attrs)
                            old_distance = new_distance
                            new_distance = attrs['tachometer']
                            new_speed = (new_distance - old_distance) * 3.6 * 5.31 / 1000
                            print(f'distance => {new_distance * 5.31 /1000} m')
                            print(f'speed => {new_speed} km/h')
                        except:
                            pass

                    count = count+1
                    ser.write(pyvesc.encode(SetRPM(rpm)))

        except KeyboardInterrupt:
            # Turn Off the VESC
            ser.write(pyvesc.encode(SetCurrent(0)))



if __name__ == "__main__":
    
   motorStart = multiprocessing.Process(target=get_values_example,args=(values,))
   motorStart.start()

