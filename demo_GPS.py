from machine import Pin, UART
import time
import re
import ssd1306
import framebuf

# Initialize UART
uart1 = UART(0, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1), timeout=1000)

i2c = machine.SoftI2C(scl=machine.Pin(17), sda=machine.Pin(16))

oled_width = 128
oled_height = 32
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.fill(0)
oled.text('Waiting...', 0, 0)

oled.show()

time.sleep(2)

def extract_coordinates(sentence):
    # Initialize variables with default values
    latitude = None
    latitude_direction = None
    longitude = None
    longitude_direction = None
    
    # Regular expression pattern to match the coordinate information
    coordinate_pattern = r'\$GNGGA,\d+\.\d+,(\d+\.\d+),([NS]),(\d+\.\d+),([EW])'
    
    # Search for the pattern in the sentence
    coordinate_match = re.search(coordinate_pattern, sentence)
    
    # Extract coordinates if pattern is found
    if coordinate_match:
        latitude = float(coordinate_match.group(1))
        latitude_direction = coordinate_match.group(2)
        longitude = float(coordinate_match.group(3))
        longitude_direction = coordinate_match.group(4)
    
    return latitude, latitude_direction, longitude, longitude_direction


while True:
    new_msg = uart1.readline()
    if new_msg:
        try:
            new_msg_str = new_msg.decode('latin-1')
        except UnicodeError:
            # Handle decoding error
            continue
        
        latitude, latitude_direction, longitude, longitude_direction = extract_coordinates(new_msg_str)
        
        # Check if any of the coordinates are not None before printing
        if latitude is not None and longitude is not None:
            print("Latitude:", latitude, latitude_direction)
            print("Longitude:", longitude, longitude_direction)
            print()
            oled.fill(0)
            oled.text(str(latitude), 0, 0)
            oled.text(str(longitude), 0, 16)
            oled.show()
        time.sleep(0.5)
        
