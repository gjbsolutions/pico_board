# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-web-server-micropython/

# Import necessary modules
import network
import socket
import time
import random
from machine import Pin
import ssd1306
import framebuf

# Otherwise you can't access pico with thonny when replugged. 
print ("Please wait, 1 seconds delay...")
time.sleep(1)

# Create an LED object on pin 'LED'
led = Pin('LED', Pin.OUT)

# OLED Screen Setup
i2c = machine.SoftI2C(scl=machine.Pin(17), sda=machine.Pin(16))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# HC12 Setup
uart = machine.UART(1, 9600, tx=machine.Pin(8), rx=machine.Pin(9), timeout=400)

# HC12 Set pin GP18 to output mode
pin = machine.Pin(18, machine.Pin.OUT)

# Set the pin to 0 (low) for AT
pin.value(1)

# Wi-Fi credentials
ssid = 'gphone'
password = '123456'  #put your ssid and password


# HTML template for the webpage
def webpage(random_value, state):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Raspberry Pi Pico Web Server</h1>
            <h2>Led Control</h2>
            <form action="./lighton">
                <input type="submit" value="Light on" />
            </form>
            <br>
            <form action="./lightoff">
                <input type="submit" value="Light off" />
            </form>
            <p>LED state: {state}</p>
            <h2>Fetch New Value</h2>
            <form action="./value">
                <input type="submit" value="Fetch value" />
            </form>
            <p>Fetched value: {random_value}</p>
            <h2>Joystick Control</h2>
            <center><b>
            <form action="./forward">
            <input type="submit" value="Forward" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Left" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./stop">
            <input type="submit" value="Stop" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Right" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            <form action="./back">
            <input type="submit" value="Back" style="height:120px; width:120px" />
            </form>
        </body>
        </html>
        """
    return str(html)

# Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for Wi-Fi connection
connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() >= 3:
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

# Check if connection is successful
if wlan.status() != 3:
    raise RuntimeError('Failed to establish a network connection')
else:
    print('Connection successful!')
    network_info = wlan.ifconfig()
    print('IP address:', network_info[0])
    oled.fill(0)
    oled.text(network_info[0], 0, 0)
    oled.show()

# Set up socket and start listening
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen()

print('Listening on', addr)

# Initialize variables
state = "OFF"
random_value = 0

# Main loop to listen for connections
while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        
        # Receive and parse the request
        request = conn.recv(1024)
        request = str(request)
        print('Request content = %s' % request)

        try:
            request = request.split()[1]
            print('Request:', request)
        except IndexError:
            pass
        
        # Process the request and update variables
        if request == '/lighton?':
            print("LED on")
            uart.write('LED_ON')
            led.value(1)
            state = "ON"
        elif request == '/lightoff?':
            print("LED off")
            uart.write('LED_OFF')
            led.value(0)
            state = 'OFF'
        elif request == '/value?':
            random_value = random.randint(0, 20)
        elif request == '/forward?':
            uart.write('Forward')
        elif request == '/back?':
            uart.write('Back')
        elif request == '/left?':
            uart.write('Left')
        elif request == '/right?':
            uart.write('Right')
        elif request == '/stop?':
            uart.write('Stop')

        # Generate HTML response
        response = webpage(random_value, state)  

        # Send the HTTP response and close the connection
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')