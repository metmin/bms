#!/usr/bin/env python3
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

time.sleep(2)
while True:
    time.sleep(5)
    print('data gonderiliyor...')
    ser.write('a'.encode('utf-8'))
    print('data gonderildi.')
   
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            f = open("battery.txt", "w")
            f.write(line)
            f.close()
            print(line)
            break