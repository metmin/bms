import serial
import pyvesc
from pyvesc.VESC.messages import GetValues, SetRPM, SetCurrent, SetRotorPositionMode, GetRotorPosition
import serial
import time
import datetime
import numpy as np
# import Adafruit_ADS1x15
from time import sleep
import multiprocessing
import RPi.GPIO as GPIO
# import pigpio
GPIO.setmode(GPIO.BCM)

# adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

# GPIO.setup(26, GPIO.IN)
# GPIO.setup(26, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

RX = 23#Change port on raspi (No need to TX) Samir

# pi = pigpio.pi()
# pi.set_mode(RX, pigpio.INPUT)
# pi.bb_serial_read_open(RX, 115200)

dist = multiprocessing.Value("d", 0)
velocity = multiprocessing.Value("f", 0)

serialport = '/dev/ttyACM0'
values = multiprocessing.Array("f",range(4))


def get_values_example(values):
    rpm = 3000
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
                    new_time = time.time()
                    diff = int (new_time - old_time)
                    if diff >= 1:
                        rpm += 500
                        print(f'rpm => {rpm}')
                        old_time = time.time()
                        ser.write(pyvesc.encode_request(GetValues))
                        (response, consumed) = pyvesc.decode(ser.read(78))
                        try:
                            attrs = vars(response)
                            #print(attrs)
                            old_distance = new_distance
                            new_distance = attrs['tachometer']
                            new_speed = (new_distance - old_distance) * 5.31 / 1000
                            print(f'distance => {new_distance * 5.31 /1000} m')
                            print(f'speed => {new_speed} m/s')
                        except:
                            pass


                    count = count+1
                    ser.write(pyvesc.encode(SetRPM(rpm)))

                    if rpm > 10000:
                        break
                # Request the current measurement from the vesc
                ser.write(pyvesc.encode_request(GetValues))
                (response, consumed) = pyvesc.decode(ser.read(78))
                try:
                    print(response)
                except:
                    pass

        except KeyboardInterrupt:
            # Turn Off the VESC
            ser.write(pyvesc.encode(SetCurrent(0)))

def speed(velocity):
    ArdSer = serial.Serial('/dev/ttyACM1',115200)
    
    while(True):    
#         read_serial=ArdSer.readline()
        s = str(ArdSer.readline())
        s1 = float(s[2:-5])
        s2 = bool(s[-4:-3])
        velocity.value = float(s1)
        print(velocity.value)

def lidar(dist):
    try:
        while True:
            time.sleep(0.05)	#This is threshold don't del Samir 
            (count, recv) = pi.bb_serial_read(RX)
            if count > 8:
              for i in range(0, count-9):
                if recv[i] == 89 and recv[i+1] == 89: # 0x59 is 89
                  checksum = 0
                  for j in range(0, 8):
                    checksum = checksum + recv[i+j]
                  checksum = checksum % 256
                  if checksum == recv[i+8]:
                    distance = recv[i+2] + recv[i+3] * 256
                    strength = recv[i+4] + recv[i+5] * 256
                    dist.value = distance
                    
                
    except:  
        pi.bb_serial_read_close(RX)
        pi.stop()

if __name__ == "__main__":
    
#    speedStart = multiprocessing.Process(target=speed,args=(velocity,))
    motorStart = multiprocessing.Process(target=get_values_example,args=(values,))
#     lidarStart = multiprocessing.Process(target=lidar,args=(dist,))

#    speedStart.start()
    motorStart.start()
#     lidarStart.start()

#    speedStart.join()
#     motorStart.join()
#     lidarStart.join()

