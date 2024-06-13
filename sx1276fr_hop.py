from machine import Pin, SPI
from sx127x import SX127x
import time
import uhashlib
import ubinascii
import struct

# Function to generate HMAC-SHA256 and truncate to 6 bytes
def generate_hmac(key, message):
    h = uhashlib.sha256(key)
    h.update(message)
    hmac = h.digest()
    return hmac[:6]

# Function to verify HMAC
def verify_hmac(key, message):
    received_data = message[:-6]
    received_hmac = message[-6:]
    expected_hmac = generate_hmac(key, received_data)
    return received_hmac == expected_hmac

# Function to create an 8-byte packet with a 3-byte counter
def create_packet(counter, payload):
    # Ensure the counter is 3 bytes and payload is 5 bytes to fit in the 8-byte packet
    counter_bytes = struct.pack('>I', counter)[-3:]  # Take the last 3 bytes of a 4-byte integer
    payload_bytes = payload[:5] + b'\x00' * (5 - len(payload))  # Ensure the payload is exactly 5 bytes
    return counter_bytes + payload_bytes

# Define the pins connected to the SX1276
spi = SPI(0, baudrate=10000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))

pins = {
    "ss": 17,    # Chip Select
    "reset": 0,  # Reset
    "dio_0": 1   # DIO0
}

# Reset the SX1276 module
reset = Pin(pins["reset"], Pin.OUT)
reset.value(0)
time.sleep(0.1)
reset.value(1)
time.sleep(0.1)

# Initialize parameters (optional, can use defaults)
parameters = {
    "frequency": 433500000,  # Initial frequency
    "tx_power_level": 1,
    "signal_bandwidth": 125e3,
    "spreading_factor": 7,
    "coding_rate": 5,
    "preamble_length": 8,
    "sync_word": 0x12,
    "enable_CRC": True,
    "invert_IQ": False
}

# Initialize the SX1276
lora = SX127x(spi, pins, parameters)

# Check if the module responds with a valid version
version = lora.readRegister(0x42)
print("SX version: {}".format(version))

if version != 0x12:  # 0x12 is the expected version for SX1276
    print("Failed to initialize SX1276, check wiring and connections.")
else:
    # Function to send data
    def send_lora_message(message):
        lora.println(message)
        print("Message sent: ", ubinascii.hexlify(message))

    # Function to receive data
    def receive_lora_message():
        if lora.received():
            received_message = lora.receive()
            print("Message received: ", ubinascii.hexlify(received_message))
            return received_message
        return None

    # Frequencies to hop between
    frequencies = [433500000, 434500000]  # Define your two frequencies here

    # Example counter and payload
    counter = 1
    payload = b'ABCDE'
    # Your 8-byte pairing key
    pairing_key = b'secret12'
    
    while True:
        # Create the 8-byte packet
        data = create_packet(counter, payload)
        counter += 1
        
        # Generate HMAC and append it to the data
        hmac = generate_hmac(pairing_key, data)
        message = data + hmac
        
        for freq in frequencies:
            lora.setFrequency(freq)  # Change frequency
            send_lora_message(message)
            time.sleep(0.050)  # 50 milliseconds delay
        
        # Simulate receiving the message for testing (comment this out in real deployment)
        received_message = message  # Simulated received message
        # received_message = receive_lora_message()  # Uncomment this in real deployment
        
        if received_message:
            if verify_hmac(pairing_key, received_message):
                print("Data is valid and authenticated")
                received_data = received_message[:-6]
                received_counter = struct.unpack('>I', b'\x00' + received_data[:3])[0]  # Unpack counter
                received_payload = received_data[3:].rstrip(b'\x00')  # Trim padding
                print("Received Counter:", received_counter)
                print("Received Payload:", received_payload)
            else:
                print("Data is invalid or corrupted")
        
        time.sleep(0.050)  # Wait before sending the next message
