from machine import UART, Pin

rxData = bytes()

uart = UART("/dev/ttyAMA0", baudrate = 9600, tx=Pin(0), rx=Pin(1))
in1 = Pin(11, Pin.OUT)
in2 = Pin(13, Pin.OUT)

in1.value(1)
in2.value(0)
uart.write("Sistem başlıyor.")


while True:
    if uart.any() > 0:
        rxData = uart.read(1);
        
        if "1" in rxData:
               uart.write("Led 1 ve Led 2 açıldı")
               print("Led 1 ve Led 2 açıldı")
               in1.value(0)
               in2.value(0)
        elif "0" in rxData:
               uart.write("Led 1 ve Led 2 kapandı")
               print("Led 1 ve Led 2 kapandı")
               in1.value(1)
               in2.value(1)
