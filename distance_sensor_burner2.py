# Untitled - By: arw_2 - Wed Mar 22 2023

import sensor, image, time, pyb, machine

from machine import SoftI2C, Pin

i2c = SoftI2C(scl=Pin('P4'),sda=Pin('P5'),freq=400000)
#i2c = I2C(2)
#i2c.init(mode=I2C.CONTROLLER,baudrate=400000)

data_ready = Pin('P3', Pin.IN)
buff = bytearray(10)

# Wait for i2c to be ready
print('I2C Scan:', i2c.scan(), '\n')
# print('Is 0x70 ready?', i2c.is_ready(0x70),'\n')

# Check if data ACK bit is high
print('Data Ready?')
print(data_ready.value(),'\n')

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
i2c.readinto(packet)
for i in range(len(packet)):
    print(packet[i])

print('\n')

# Set Mode
print('Sending setModePacket')
i2c.start()
buff[0] = 0x00
buff[1] = 0xE1
buff[2] = 0x00
buff[3] = 0x00
buff[4] = 0x00
buff[5] = 0x00
buff[6] = 0x5C
buff[7] = 0xD8
buff[8] = 0x26
buff[9] = 0x06
i2c.write(buff)
i2c.stop()
pyb.delay(20)
print('\n')

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
i2c.readinto(packet)
for i in range(len(packet)):
    print(packet[i])

print('\n')

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
i2c.readinto(packet)
for i in range(len(packet)):
    print(packet[i])

print('\n')

# Write readVersionPacket
print('Writing readVersionPacket')
i2c.start()
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x43
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x55
i2c.write(buff)
buff[0] = 0x10
i2c.write(buff)
buff[0] = 0xCD
i2c.write(buff)
buff[0] = 0x9A
i2c.write(buff)
i2c.stop()
pyb.delay(20)
print('\n')

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
i2c.readinto(packet)
for i in range(len(packet)):
    print(packet[i])

print('\n')

# Start Filter
print('Sending startFilterPacket')
i2c.start()
buff[0] = 0xF5
i2c.write(buff)
buff[0] = 0xD9
i2c.write(buff)
buff[0] = 0x01
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0xB7
i2c.write(buff)
buff[0] = 0x1F
i2c.write(buff)
buff[0] = 0xBA
i2c.write(buff)
buff[0] = 0xBA
i2c.write(buff)
i2c.stop()
pyb.delay(20)
print('\n')

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
i2c.readinto(packet)
for i in range(len(packet)):
    print(packet[i])

print('\n')

# Set Mode
print('Sending setModePacket')
i2c.start()
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0xE1
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x5C
i2c.write(buff)
buff[0] = 0xD8
i2c.write(buff)
buff[0] = 0x26
i2c.write(buff)
buff[0] = 0x06
i2c.write(buff)
i2c.stop()
pyb.delay(20)
print('\n')

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(12)
i2c.readinto(packet)
for i in range(len(packet)):
    print(packet[i])

print('\n')

# Start Measure
print('Sending startPacket')
i2c.start()
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0xE0
i2c.write(buff)
buff[0] = 0x01
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x66
i2c.write(buff)
buff[0] = 0x25
i2c.write(buff)
buff[0] = 0x46
i2c.write(buff)
buff[0] = 0x93
i2c.write(buff)
i2c.stop()
pyb.delay(20)
print('\n')

#while(data_ready.value() == 0):
#    print('Waiting for data to be ready')
#    pyb.delay(100)
# print('Data Ready?')
print(data_ready.value(),'\n')

# Get value
print('Getting Value')
packet = bytearray(24)
i2c.readinto(packet)
for i in range(len(packet)):
    print(packet[i])

print('\n')

# Send Error Readout Packet
print('Sending errorReadoutPacket')
i2c.start()
buff[0] = 0xF5
i2c.write(buff)
buff[0] = 0x65
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x00
i2c.write(buff)
buff[0] = 0x9A
i2c.write(buff)
buff[0] = 0x08
i2c.write(buff)
buff[0] = 0xE9
i2c.write(buff)
buff[0] = 0x8A
i2c.write(buff)
i2c.stop()
pyb.delay(20)


# Wait for ACK bit
# while(data_ready.value() == 0):
#     print('Waiting for data to be ready')
#     pyb.delay(100)
print('Data Ready?')
print(data_ready.value())

# Receive Error Readout Data
print('Reading Error Readout')
packet = bytearray(12)
i2c.readinto(packet)
for i in range(len(packet)):
    print(packet[i])

print('\n')

