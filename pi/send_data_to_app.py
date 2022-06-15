import serial
from time import sleep
import json
import random

def manipulate_data(data, speed):
    #print(data)
    data = data.replace('=', '":').replace(',', ',"').replace('.0','')
    data = '{"' + data + '}'
    data_json = json.loads(data)
    
    # set the speed
    data_json['speed'] = speed
    
    # get batvolt as persentage
    data_json['batvolt'] = int ((int (data_json['batvolt']) - 30000) / 120)
    
    return(json.dumps(data_json))

def get_speed():
    return random.randint(0,25)

ser = serial.Serial("/dev/ttyUSB0", 9600)  # Open port with baud rate
while True:

    
    print('data aliniyor...')
    received_data = ser.read()              #read serial port
    sleep(1)
    while 1:
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        if data_left <= 0:
            break
    print(received_data.decode())

    print('data alindi.')
    print (received_data)

    f = open("battery.txt", "r")
    data = f.read()
    f.close()

    speed = get_speed()
    manupilated_data = manipulate_data(data, speed)
    print('data gonderiliyor...')
    #print(manupilated_data)
    ser.write((manupilated_data + '\r\n').encode())  # transmit data serially
    print('data gonderildi.')
    
    ser.flushInput()
    #break
