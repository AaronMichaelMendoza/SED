# Untitled - By: arw_2 - Wed Apr 12 2023

import sensor, image, time, pyb, machine

from machine import UART, Pin

CM_TO_FT = 0.0328084

uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

packet = bytearray(1)
packet[0] = 0x42
uart.write(packet)
packet[0] = 0x57
uart.write(packet)
packet[0] = 0x02
uart.write(packet)
packet[0] = 0x00
uart.write(packet)
packet[0] = 0x00
uart.write(packet)
packet[0] = 0x00
uart.write(packet)
packet[0] = 0x01
uart.write(packet)
packet[0] = 0x06
uart.write(packet)


while(True):
    if(uart.any()):
        bytes = uart.read()
        if(len(bytes) == 9):
            print('Distance (ft):', ((bytes[3]*256) + (bytes[2])) * CM_TO_FT)
            print('Signal Strength:', (bytes[5]*256) + (bytes[4]))

    pyb.delay(10)


