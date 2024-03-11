from machine import I2C, Pin
import time
import math
 
# HMC5883L address and register addresses
HMC5883L_ADDR = 0x1E
CONFIG_REG_A = 0x00
CONFIG_REG_B = 0x01
MODE_REG = 0x02
DATA_REG = 0x03
 
# Conversion factor from raw value to uT
# With default gain 1 Ga = 1090 LSb
# And 1 Ga = 100 uT, therefore 1 LSb = 100 uT / 1090 LSb
LSB_TO_UT = 100.0 / 1090.0
 
# Initialize I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
 
# Check if HMC5883L is connected
if HMC5883L_ADDR not in i2c.scan():
    raise ValueError('HMC5883L not found')
 
# Write configuration to HMC5883L
# Continuous measurement mode, 15Hz data output rate
i2c.writeto_mem(HMC5883L_ADDR, CONFIG_REG_A, bytes([0x70]))
i2c.writeto_mem(HMC5883L_ADDR, CONFIG_REG_B, bytes([0x20]))
i2c.writeto_mem(HMC5883L_ADDR, MODE_REG, bytes([0x00]))
 
while True:
    data = i2c.readfrom_mem(HMC5883L_ADDR, DATA_REG, 6)
    x = ((data[0] << 8) | data[1])
    z = ((data[2] << 8) | data[3])
    y = ((data[4] << 8) | data[5])
    
    if x > 32767:
        x -= 65536
    if y > 32767:
        y -= 65536
    if z > 32767:
        z -= 65536
 
    # Convert to uT
    x *= LSB_TO_UT
    y *= LSB_TO_UT
    z *= LSB_TO_UT
 
    # Calculate heading in degrees
    heading = math.atan2(y, x)
    
    # Convert radian to degree
    heading = math.degrees(heading)
    
    # Due to declination, the heading may need to be corrected
    # Declination is the error between magnetic north and true north, depending on your geographical location. 
    # Here, let's assume we have a declination of 0 degrees. If you know the declination in your area, put it instead.
    declination_angle = 0.0
    heading += declination_angle
    
    # Correct negative values
    if heading < 0:
        heading += 360
    
    print("Magnetic field in X: %.2f uT, Y: %.2f uT, Z: %.2f uT, Heading: %.2f°" % (x, y, z, heading))
    time.sleep(0.1)