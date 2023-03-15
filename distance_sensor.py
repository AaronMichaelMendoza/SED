# File:          distance_sensor.py
# Description:   This script holds the functions used to interface with the distance sensor.
# Authors:       C. Jackson, J. Markle, C. McCarver, A. Mendoza, A. White, H. Williams
# Date Created:  3/3/2023
# Last Modified: 3/15/2023

import sensor, image, time, pyb
from pyb import I2C

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

i2c = I2C(2) #initialize I2C bus 2
i2c.scan() # returns list of slave addresses

def readDistance():
    i2c.send(1, 0x70) # send 1 byte to slave with address 0x70
    i2c.recv(byte, 0x70) # receive 1 byte from slave



#i2c.mem_read(2, 0x42, 0x10) # read 2 bytes from slave 0x42, slave memory 0x10
#i2c.mem_write('xy', 0x42, 0x10) # write 2 bytes to slave 0x42, slave memory 0x10

clock = time.clock()

while(True):
   readDistance()
