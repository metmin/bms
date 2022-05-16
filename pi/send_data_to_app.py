import serial
from time import sleep
import json


def manipulate_data(data):
    data = data.replace('=', '":"').replace(',', '","')
    data = '{"' + data + '"}'
    return(json.dumps(json.loads(data)))


ser = serial.Serial("/dev/ttyUSB1", 9600)  # Open port with baud rate
while True:

    f = open("data.txt", "r")
    data = f.read()
    f.close()

    manupilated_data = manipulate_data(data)
    print(manupilated_data)
    ser.write(manupilated_data)  # transmit data serially
    sleep(0.5)
    #break
