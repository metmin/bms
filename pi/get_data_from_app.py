import serial
from time import sleep
import json
import random


ser = serial.Serial("/dev/ttyUSB0", 9600)  # Open port with baud rate
while True:
    print('data aliniyor...')
    received_data = ser.readline()
    print('data alindi.')
    print (received_data)
    #break
