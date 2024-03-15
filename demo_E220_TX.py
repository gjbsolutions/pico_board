# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E220 LoRa module with MicroPython.
# Sending string to a specified address (receiver)
# ADDH = 0x00
# ADDL = 0x02
# CHAN = 23
#
# Note: This code was written and tested using MicroPython on an ESP32 board.
#       It works with other boards, but you may need to change the UART pins.

from machine import UART

from lora_e220 import LoRaE220, Configuration
from lora_e220_constants import FixedTransmission, RssiEnableByte
from lora_e220_operation_constant import ResponseStatusCode

# Initialize the LoRaE220 module
uart1 = UART(1, 9600)
lora = LoRaE220('400T22D', uart1, aux_pin=2, m0_pin=16, m1_pin=17)
code = lora.begin()
print("Initialization: {}", ResponseStatusCode.get_description(code))


# Send a string message (fixed)
message = 'Hello World!'
code = lora.send_fixed_message(0, 0x01, 23, message)
# The receiver must be configured with ADDH = 0x00, ADDL = 0x01, CHAN = 23
print("Send message: {}", ResponseStatusCode.get_description(code))

