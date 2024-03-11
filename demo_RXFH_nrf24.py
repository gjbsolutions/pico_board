# Rx FH code

import ustruct as struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from micropython import const

# pin definition for the Raspberry Pi Pico
led = Pin(25, Pin.OUT)
cfg = {"spi": 1, "miso": 12, "mosi": 15, "sck": 14, "csn": 13, "ce": 10}

# delay between receiving a message and waiting for the next message
POLL_DELAY = const(15)
# Delay between receiving a message and sending the response
SEND_DELAY = const(10)

# Addresses
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

# Channels List
chn = [46, 98, 102]

# Use hopping if true, else use first channel in List
usehopping = True

# channel index from List
i = 0

ct = 1
frhop = 1

# initialize
csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
spi = SPI(1, sck=Pin(cfg["sck"]), mosi=Pin(cfg["mosi"]), miso=Pin(cfg["miso"]))
nrf = NRF24L01(SPI(cfg["spi"]), csn, ce, payload_size=8)
nrf.open_tx_pipe(pipes[1])
nrf.open_rx_pipe(1, pipes[0])
nrf.set_channel(int(chn[i]))
nrf.start_listening()
print("nRF24L01 receiver;", "Channel", i, "waiting for the first post...")

receive_time = utime.ticks_ms()
while True:
    if utime.ticks_diff(utime.ticks_ms(), receive_time) > 50:
        i += 1
        if i >= len(chn):
            i = 0
        nrf.set_channel(int(chn[i]))
        nrf.start_listening()
        receive_time = utime.ticks_ms()
        print("nRF24L01 receiver;", "Channel", i, "waiting for the first post...")
        frhop = frhop + 1
    if nrf.any(): # we received something
        while nrf.any():
            buf = nrf.recv()
            counter = struct.unpack("i", buf)
            print("message received:", counter[0])
            ct = ct + 1
            utime.sleep_ms(POLL_DELAY) # delay before next listening

        # response = counter[0]%2 # preparing the response
        # utime.sleep_ms(SEND_DELAY) # Give the other Pico a brief time to listen
        # nrf.stop_listening()
        # try:
            # nrf.send(struct.pack("i", response))
        # except OSError:
            # pass
        # print("reply sent:", response)
        
        receive_time = utime.ticks_ms()
        if usehopping == True:
            i += 1
            if i >= len(chn):
                i = 0
            nrf.set_channel(int(chn[i]))
            frhop = frhop + 1
        nrf.start_listening()

