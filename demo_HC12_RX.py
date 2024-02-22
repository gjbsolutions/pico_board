import machine
import time

# Define UART pins
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))


while True:
    if uart.any():
        line = uart.readline().decode("utf-8")
        print(line)
        time.sleep(0.5)  # Adjust the delay as needed
