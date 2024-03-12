from machine import Pin, UART
import time

uart = UART(1, 9600, tx=Pin(8), rx=Pin(9), timeout=400)

# HC12 Set pin GP18 to output mode
pin = Pin(18, Pin.OUT)

# Set the pin to 0 (low) for AT
pin.value(1)

# Press Key2 to enter sending mode
key2button_pin = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    if not key2button_pin.value():
        user_input = input("Enter a command : ")
        uart.write(user_input.encode())  # Send the user input over UART
    
    if uart.any():
        data = uart.read()
        print(data)
    
    time.sleep(1)