# Untitled - By: arw_2 - Mon Mar 27 2023

import sensor, image, time, pyb, machine

from pyb import I2C, Pin

i2c = I2C(2)
i2c.init(mode=I2C.CONTROLLER, baudrate=400000)

print(i2c.scan())
pyb.delay(100)

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
i2c.send(buff, 0x70, timeout=5000)
pyb.delay(20)
i2c.send(buff[1], 0x70, timeout=5000)
i2c.send(buff[2], 0x70, timeout=5000)
i2c.send(buff[3], 0x70, timeout=5000)
i2c.send(buff[4], 0x70, timeout=5000)
i2c.send(buff[5], 0x70, timeout=5000)
i2c.send(buff[6], 0x70, timeout=5000)
i2c.send(buff[7], 0x70, timeout=5000)
i2c.send(buff[8], 0x70, timeout=5000)
pyb.delay(20)

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(11)
i2c.recv(packet, 0x70)
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
i2c.send(buff, 0x70)
pyb.delay(20)
print('\n')

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(11)
i2c.recv(packet, 0x70)
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
i2c.send(buff, 0x70)
print('Number of ACKs:', num_acks)
pyb.delay(20)

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(11)
i2c.recv(packet, 0x70)
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
i2c.send(buff, 0x70)
print('Number of ACKs:', num_acks)
pyb.delay(20)

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(11)
i2c.recv(packet, 0x70)
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
i2c.send(buff, 0x70)
print('Number of ACKs:', num_acks)
pyb.delay(20)

#Clear serial port cache
print('Clearing Serial Port Cache:')
packet = bytearray(23)
i2c.recv(packet, 0x70)
for i in range(len(packet)):
    print(packet[i])
