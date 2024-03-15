from machine import UART, Pin
import utime

m0 = Pin(16,Pin.OUT)
m1 = Pin(17,Pin.OUT)

m0.value(0)
m1.value(0)

uart1 = UART(1, 9600)

print("Hi, I'm going to send message!")
 
uart1.write("Hello, world?")
utime.sleep_ms(500)
 
while True:
    if uart1.any():
        char = uart1.read(1).decode('utf-8')
        print(char, end='')