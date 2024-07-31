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

def send_at_command(command):
    """Send an AT command to the E290 module and return the response."""
    uart.write(command)
    time.sleep(0.1)
    response = uart.read()
    return response

def send_message(message):
    """Send a message using the E290 module."""
    uart.write(message + '\r\n')  # Adding '\r\n' might not be necessary but can help with some modules
    time.sleep(0.1)  # Allow time for the message to be sent

if __name__ == "__main__":
    # Set mode to Sleep (Configuration) Mode (Mode 3)
    set_mode(0, 1)
    print("Set to Configuration Mode (Mode 3)")

    # Give the module some time to enter configuration mode
    time.sleep(1)

    # Example AT commands
    commands = [
        ("AT+HELP=?", "Query AT command table"),
        ("AT+ADDR=?", "Query module address"),
        ("AT+CHANNEL=?", "Query module working channel"),
        ("AT+NETID=?", "Query Network ID")
    ]

    for command, description in commands:
        response = send_at_command(command)
        print(f"{description} ({command}): {response}")

    # Return to Normal Mode (Mode 0)
    set_mode(0, 0)
    print("Set to Normal Mode (Mode 0)")
    
     # Give the module some time to enter normal mode
    time.sleep(1)

    # Send a message
    message = "Hello, World!"
    send_message(message)
    print(f"Message sent: {message}")   
