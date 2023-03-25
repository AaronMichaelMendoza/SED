# Untitled - By: arw_2 - Wed Mar 22 2023

import sensor, image, time, pyb, machine

from machine import I2C, Pin

i2c = I2C(scl=Pin('P4'),sda=Pin('P5'),freq=400000)

data_ready = Pin('P3', Pin.IN)
buff = bytearray(1)

# Wait for i2c to be ready
print('I2C Scan:', i2c.scan(), '\n')
#while(i2c.scan() == []):
#    print('Waiting')
#    pyb.delay(10)
#print(i2c.scan(),'\n')

# Check if data ACK bit is high
print('Data Ready?')
print(data_ready.value(),'\n')

# Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
packet[0]=0xFA
read_buff = [0,0,0,0,0,0,0,0,0,0,0]
for i in range(11):
    try:
        read_buff[i] = i2c.readfrom(0x70,1)
    except:
        print('Read Failed\n')
    print(read_buff[i])
print('\n')

# Set Mode
print('Sending setModePacket')
buff[0] = 0xF5
i2c.writeto(0x70,buff)
buff[0] = 0xE1
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0xA5
i2c.writeto(0x70,buff)
buff[0] = 0x8D
i2c.writeto(0x70,buff)
buff[0] = 0x89
i2c.writeto(0x70,buff)
buff[0] = 0xA7
i2c.writeto(0x70,buff)
pyb.delay(20)
print('\n')

# Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
packet[0]=0xFA
read_buff = [0,0,0,0,0,0,0,0,0,0,0]
for i in range(11):
    read_buff[i] = i2c.readfrom(0x70,1)
    print(read_buff[i])
print('\n')

# Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
packet[0]=0xFA
read_buff = [0,0,0,0,0,0,0,0,0,0,0]
for i in range(11):
    read_buff[i] = i2c.readfrom(0x70,1)
    print(read_buff[i])
print('\n')

# Write readVersionPacket
print('Writing readVersionPacket')
buff[0] = 0xF5
i2c.writeto(0x70,buff)
buff[0] = 0x43
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0xAC
i2c.writeto(0x70,buff)
buff[0] = 0x45
i2c.writeto(0x70,buff)
buff[0] = 0x62
i2c.writeto(0x70,buff)
buff[0] = 0x3B
i2c.writeto(0x70,buff)
pyb.delay(20)
print('\n')

# Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
packet[0]=0xFA
read_buff = [0,0,0,0,0,0,0,0,0,0,0]
for i in range(11):
    read_buff[i] = i2c.readfrom(0x70,1)
    print(read_buff[i])
print('\n')

# Start Filter
print('Sending startFilterPacket')
buff[0] = 0xF5
i2c.writeto(0x70,buff)
buff[0] = 0xD9
i2c.writeto(0x70,buff)
buff[0] = 0x01
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0xB7
i2c.writeto(0x70,buff)
buff[0] = 0x1F
i2c.writeto(0x70,buff)
buff[0] = 0xBA
i2c.writeto(0x70,buff)
buff[0] = 0xBA
i2c.writeto(0x70,buff)
pyb.delay(20)
print('\n')

# Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
packet[0]=0xFA
read_buff = [0,0,0,0,0,0,0,0,0,0,0]
for i in range(11):
    read_buff[i] = i2c.readfrom(0x70,1)
    print(read_buff[i])
print('\n')

# Set Mode
print('Sending setModePacket')
buff[0] = 0xF5
i2c.writeto(0x70,buff)
buff[0] = 0xE1
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0xA5
i2c.writeto(0x70,buff)
buff[0] = 0x8D
i2c.writeto(0x70,buff)
buff[0] = 0x89
i2c.writeto(0x70,buff)
buff[0] = 0xA7
i2c.writeto(0x70,buff)
pyb.delay(20)
print('\n')

# Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
packet[0]=0xFA
read_buff = [0,0,0,0,0,0,0,0,0,0,0]
for i in range(11):
    read_buff[i] = i2c.readfrom(0x70,1)
    print(read_buff[i])
print('\n')

# Start Measure
print('Sending startPacket')
buff[0] = 0xF5
i2c.writeto(0x70,buff)
buff[0] = 0xE0
i2c.writeto(0x70,buff)
buff[0] = 0x01
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x9F
i2c.writeto(0x70,buff)
buff[0] = 0x70
i2c.writeto(0x70,buff)
buff[0] = 0xE9
i2c.writeto(0x70,buff)
buff[0] = 0x32
i2c.writeto(0x70,buff)
pyb.delay(20)
print('\n')

while(data_ready.value() == 0):
    print('Waiting for data to be ready')
    pyb.delay(100)
print('Data Ready?')
print(data_ready.value(),'\n')

# Get value
print('Getting Value')
packet = bytearray(24)
packet[0]=0xFA
read_buff = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(23):
    read_buff[i] = i2c.readfrom(0x70,1)
    print(read_buff[i])
print('\n')

# Send Error Readout Packet
print('Sending errorReadoutPacket')
buff[0] = 0xF5
i2c.writeto(0x70,buff)
buff[0] = 0x65
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x00
i2c.writeto(0x70,buff)
buff[0] = 0x9A
i2c.writeto(0x70,buff)
buff[0] = 0x08
i2c.writeto(0x70,buff)
buff[0] = 0xE9
i2c.writeto(0x70,buff)
buff[0] = 0x8A
i2c.writeto(0x70,buff)
pyb.delay(20)


# Wait for ACK bit
while(data_ready.value() == 0):
    print('Waiting for data to be ready')
    pyb.delay(100)
print('Data Ready?')
print(data_ready.value())

# Receive Error Readout Data
packet = bytearray(12)
packet[0]=0xFA
read_buff = [0,0,0,0,0,0,0,0,0,0,0]
for i in range(11):
    read_buff[i] = i2c.readfrom(0x70,1)
    print(read_buff[i])


