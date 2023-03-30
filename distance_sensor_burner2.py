# Untitled - By: arw_2 - Wed Mar 22 2023

import sensor, image, time, pyb, machine

from machine import SoftI2C, Pin

i2c = SoftI2C(scl=Pin('P4'),sda=Pin('P5'),freq=400000)
#i2c = I2C(scl=Pin('P4'),sda=Pin('P5'),freq=400000)
#i2c.init(mode=I2C.CONTROLLER,baudrate=400000)

data_ready = Pin('P3', Pin.IN)
buff = bytearray(10)

# Wait for i2c to be ready
#print('I2C Scan:', i2c.scan(), '\n')
# print('Is 0x70 ready?', i2c.is_ready(0x70),'\n')

## Check if data ACK bit is high
#print('Data Ready?')
#print(data_ready.value(),'\n')
#

print('Sending setModePacket')
buff = bytearray(9)
buff[0] = 0xE1
buff[1] = 0x00
buff[2] = 0x00
buff[3] = 0x00
buff[4] = 0x00
buff[5] = 0x5C
buff[6] = 0xD8
buff[7] = 0x26
buff[8] = 0x06
i2c.start()
num_acks = i2c.writeto(0x70,buff)
i2c.stop()
print('Number of ACKs:', num_acks)
pyb.delay(20)

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(11)
i2c.readfrom_into(0x70, packet)
for i in range(len(packet)):
    print(packet[i])


print('Sending readVersionPacket')
buff = bytearray(9)
buff[0] = 0x43
buff[1] = 0x00
buff[2] = 0x00
buff[3] = 0x00
buff[4] = 0x00
buff[5] = 0x55
buff[6] = 0x10
buff[7] = 0xCD
buff[8] = 0x9A
i2c.start()
num_acks = i2c.writeto(0x70,buff)
i2c.stop()
print('Number of ACKs:', num_acks)
pyb.delay(20)
print('\n')

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(11)
i2c.readfrom_into(0x70, packet)
for i in range(len(packet)):
    print(packet[i])


print('Sending startFilterPacket')
buff = bytearray(9)
buff[0] = 0xD9
buff[1] = 0x01
buff[2] = 0x00
buff[3] = 0x00
buff[4] = 0x00
buff[5] = 0x4E
buff[6] = 0x4A
buff[7] = 0x15
buff[8] = 0x1B
i2c.start()
num_acks = i2c.writeto(0x70,buff)
i2c.stop()
print('Number of ACKs:', num_acks)
pyb.delay(20)

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(11)
i2c.readfrom_into(0x70, packet)
for i in range(len(packet)):
    print(packet[i])

print('Sending setModePacket')
buff = bytearray(9)
buff[0] = 0xE1
buff[1] = 0x00
buff[2] = 0x00
buff[3] = 0x00
buff[4] = 0x00
buff[5] = 0x5C
buff[6] = 0xD8
buff[7] = 0x26
buff[8] = 0x06
i2c.start()
num_acks = i2c.writeto(0x70,buff)
i2c.stop()
print('Number of ACKs:', num_acks)
pyb.delay(20)

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(11)
i2c.readfrom_into(0x70, packet)
for i in range(len(packet)):
    print(packet[i])

print('Sending startPacket')
buff = bytearray(9)
buff[0] = 0xE0
buff[1] = 0x01
buff[2] = 0x00
buff[3] = 0x00
buff[4] = 0x00
buff[5] = 0x66
buff[6] = 0x25
buff[7] = 0x46
buff[8] = 0x93
i2c.start()
num_acks = i2c.writeto(0x70,buff)
i2c.stop()
print('Number of ACKs:', num_acks)
pyb.delay(20)

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(23)
i2c.readfrom_into(0x70, packet)
for i in range(len(packet)):
    print(packet[i])
