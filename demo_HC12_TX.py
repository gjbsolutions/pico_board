from machine import UART
import time

uart = UART(0, 9600, timeout=400)

count = 0

while True:
    count += 1
    print(count)
    uart.write(str(count)+"\n")
    time.sleep(2)

