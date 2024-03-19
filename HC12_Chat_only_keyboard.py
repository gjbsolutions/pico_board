from machine import Pin, UART
import time
import sys
import uselect

uart = UART(1, 9600, tx=Pin(8), rx=Pin(9), timeout=400)

# HC12 Set pin GP18 to output mode
pin = Pin(18, Pin.OUT)

# Set the pin to 0 (low) for AT
pin.value(1)

spoll=uselect.poll()
spoll.register(sys.stdin,uselect.POLLIN)
def read1():
    return(sys.stdin.read(1) if spoll.poll(0) else None)

time.sleep(1)

while True:
 
    c = read1()
    if c == '^':
        user_input = input()
        uart.write(user_input.encode())  # Send the user input over UART
        
    if c == '&':
        user_input = input()
        pin.value(0)
        time.sleep(1)
        # example AT+RX
        uart.write(user_input)
        data = uart.read()
        print(data)
        pin.value(1)
        time.sleep(1)
    
    if uart.any():
        data = uart.read()
        print(data)
    
    time.sleep(1)