"""
nRF24L01 scanner
Raspberry Pi Pico and nRF24L01 module.
"""
import utime
import math
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from machine import I2C

import machine
import ssd1306
import framebuf
from time import sleep

# RF_SETUP register
POWER_0 = const(0x00)  # -18 dBm
POWER_1 = const(0x02)  # -12 dBm
POWER_2 = const(0x04)  # -6 dBm
POWER_3 = const(0x06)  # 0 dBm
SPEED_1M = const(0x00)
SPEED_2M = const(0x08)
SPEED_250K = const(0x20)

i2c = machine.SoftI2C(scl=machine.Pin(17), sda=machine.Pin(16))

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text('2.4 GHz Scanner', 0, 0)
oled.show()

led = Pin(25, Pin.OUT)

def map_to_string(value):
    # Limit the input value to a maximum of 200
    value = min(value, 100)
    
    # Define the minimum and maximum values of your input variable
    MIN_VALUE = 0
    MAX_VALUE = 100
    
    # Define the logarithmic base to use for the mapping
    LOG_BASE = 10
    
    # Calculate the logarithmic value of the input variable
    log_value = math.log(value + 1, LOG_BASE)
    
    # Map the logarithmic value to an integer between 0 and 9
    mapped_value = int(log_value * 9 / math.log(MAX_VALUE + 1, LOG_BASE))
    
    # Ensure that the mapped value is within the desired range of 0 to 15
    mapped_value = max(0, min(mapped_value, 9))
    
    return mapped_value

# Pico pin definition:
cfg = {"spi": 1, "miso": 12, "mosi": 15, "sck": 14, "csn": 13, "ce": 10}
# Addresses
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")
chn = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]	# Channels List
i = 0  				# channel index from List

# initialize
led.value(1)
utime.sleep_ms(250)
led.value(0)

csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = SPI(1, sck=Pin(cfg["sck"]), mosi=Pin(cfg["mosi"]), miso=Pin(cfg["miso"]))
nrf = NRF24L01(SPI(cfg["spi"]), csn, ce, payload_size=8)
nrf.set_power_speed(POWER_0, SPEED_2M)
nrf.set_channel(int(chn[i]))
nrf.start_listening()

print("nRF24L01 receiver scanning...")
counter = 0
offset = 0
receive_time = utime.ticks_ms()

s = ""
s2 = ""
rssi = 0

while True:
    if utime.ticks_diff(utime.ticks_ms(), receive_time) > 50:
        if offset > 4:
            print("Channel", int(chn[i]), "Noise", counter)
            if i < 15:
                s = s +  str(map_to_string(counter))
            else:
                s2 = s2 +  str(map_to_string(counter))
            rssi = rssi + counter
            if counter > 0:
                led.value(1)
            else:
                led.value(0)
            i = i + 1
            if i >= len(chn):
                i = 0
                oled.fill(0)
                s2 = s2 + ' SR ' + str(rssi)
                oled.text(s, 0, 0)
                oled.text(s2, 0, 18)
                # oled.text('rssi ' + str(rssi),0,18)
                oled.show()
                s = ""
                s2= ""
                rssi = 0
            counter = 0
            offset = 0
        else:
            nrf.set_channel(int(chn[i]) + offset)
            nrf.start_listening()
            offset = offset + 1
            receive_time = utime.ticks_ms()
    else:
        carrier_power = nrf.reg_read(0x9)
        counter = counter + carrier_power