from machine import UART, Pin
import time

# Define the GPIO pins connected to M0 and M1
M0_PIN = 2
M1_PIN = 3

# Initialize the pins
m0 = Pin(M0_PIN, Pin.OUT, value=1)  # Default to high (pull-up)
m1 = Pin(M1_PIN, Pin.OUT, value=1)  # Default to high (pull-up)

def set_mode(m0_state, m1_state):
    """Set the operating mode of the E290 module."""
    m0.value(m0_state)
    m1.value(m1_state)
    time.sleep(0.1)  # Small delay to allow the module to switch modes

# Initialize UART for communication with the E290 module
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

def clear_uart_buffer():
    """Clear the UART buffer."""
    while uart.any():
        uart.read()

def send_message(message):
    """Send a message using the E290 module."""
    uart.write(message + '\r\n')  # Adding '\r\n' might not be necessary but can help with some modules
    time.sleep(0.1)  # Allow time for the message to be sent

def receive_message():
    """Receive a message from the E290 module."""
    if uart.any():
        response = uart.read()
        if response:
            # Print the raw byte values
            print(f"Raw bytes received: {list(response)}")

            # Extract RSSI value (assuming it is the last byte)
            rssi_value = response[-1]
            
            # Extract and decode message, ignoring the RSSI byte
            decoded_message = ""
            for byte in response[:-1]:  # Exclude the last byte (RSSI)
                try:
                    decoded_message += chr(byte)
                except ValueError:
                    # Ignore bytes that can't be decoded
                    pass
            
            return decoded_message.strip(), rssi_value
    return None, None

if __name__ == "__main__":
    # Set mode to Normal Mode (Mode 0)
    set_mode(0, 0)
    print("Set to Normal Mode (Mode 0)")
    
    # Give the module some time to enter normal mode
    time.sleep(1)

    # Clear any residual data in the UART buffer
    clear_uart_buffer()

    # Send a message
    message = "Hello, World!"
    send_message(message)
    print(f"Message sent: {message}")

    # Wait for a few seconds
    time.sleep(1)


    # Start receiving messages
    print("Listening for incoming messages...")
    while True:
        received_message, rssi_value = receive_message()
        if received_message:
            print(f"Received message: {received_message}")
            print(f"RSSI value: {rssi_value}")
        time.sleep(1)  # Small delay to avoid busy waiting
