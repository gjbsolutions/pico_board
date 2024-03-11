# Tx FH code

import ustruct as struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01

# pin definition for the Raspberry Pi Pico
led = Pin(25, Pin.OUT)
cfg = {"spi": 1, "miso": 12, "mosi": 15, "sck": 14, "csn": 13, "ce": 10}

# Addresses (little endian)
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

# Channels List
chn = [46, 98, 102]

# Use hopping if true, else use first channel in List
usehopping = True

# Increase the value by 1 with each tx
counter = 0  	
errorcounter = 0

# channel index from List
i = 0
  			
# initialize
led.value(1)
utime.sleep_ms(250)
led.value(0)
print("NRF24L01 transmitter")
csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = SPI(1, sck=Pin(cfg["sck"]), mosi=Pin(cfg["mosi"]), miso=Pin(cfg["miso"]))
nrf = NRF24L01(SPI(cfg["spi"]), csn, ce, payload_size=8)
nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])
nrf.set_channel(int(chn[i]))
nrf.start_listening()

while True:
    if usehopping == True:
        if i >= len(chn):
            i = 0
        nrf.set_channel(int(chn[i]))
        nrf.start_listening()
    nrf.stop_listening()

    counter = counter + 1 
    print("channel:", i, "sending:",  counter)

    try:
        nrf.send(struct.pack("i",  counter)) 
        print('ok', (counter - errorcounter) / counter * 100)
    except OSError:
        print('error')
        errorcounter = errorcounter + 1
        pass

    # Listen if the other Pico answers us
    nrf.start_listening()
    start_time = utime.ticks_ms()
    timeout = False
    while not timeout:
        if utime.ticks_diff(utime.ticks_ms(), start_time) > 5:
            timeout = True

    if usehopping == True:
        i += 1

    # Wait before sending the next message
    utime.sleep_ms(5)