# Untitled - By: arw_2 - Wed Mar 22 2023

import sensor, image, time, pyb
from machine import I2C, Pin

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

LIDAR_ADDR = 0x70
SCL = Pin('P4')
SDA = Pin('P5')

class Lidar07:

    distance          = 0
    amplitude         = 0
    i2c               = I2C(scl=Pin('P4'), sda=Pin('P5'), freq=400000)
    readVersionPacket = bytearray(10)
    setIntervalPacket = bytearray(10)
    setModePacket     = bytearray(10)
    startPacket       = bytearray(10)
    stopPacket        = bytearray(10)
    startFilterPacket = bytearray(10)
    stopFilterPacket  = bytearray(10)
    setFreqPacket     = bytearray(10)

    def __init__(self):
        #self.i2c.init(I2C.CONTROLLER)
        #self.i2c.init(I2C.SLAVE, addr=0x70)
        pyb.delay(100)

    def begin(self):
        self.readVersionPacket[0] = 0xF5
        self.readVersionPacket[1] = 0x43
        self.readVersionPacket[2] = 0x00
        self.readVersionPacket[3] = 0x00
        self.readVersionPacket[4] = 0x00
        self.readVersionPacket[5] = 0x00
        self.readVersionPacket[6] = 0xAC
        self.readVersionPacket[7] = 0x45
        self.readVersionPacket[8] = 0x62
        self.readVersionPacket[9] = 0x3B

        self.setModePacket[0] = 0xF5
        self.setModePacket[1] = 0xE1
        self.setModePacket[2] = 0x00
        self.setModePacket[3] = 0x00
        self.setModePacket[4] = 0x00
        self.setModePacket[5] = 0x00
        self.setModePacket[6] = 0xA5
        self.setModePacket[7] = 0x8D
        self.setModePacket[8] = 0x89
        self.setModePacket[9] = 0xA7

        self.startPacket[0] = 0xF5
        self.startPacket[1] = 0xE0
        self.startPacket[2] = 0x01
        self.startPacket[3] = 0x00
        self.startPacket[4] = 0x00
        self.startPacket[5] = 0x00
        self.startPacket[6] = 0x9F
        self.startPacket[7] = 0x70
        self.startPacket[8] = 0xE9
        self.startPacket[9] = 0x32

        self.stopPacket[0] = 0xF5
        self.stopPacket[1] = 0xE0
        self.stopPacket[2] = 0x00
        self.stopPacket[3] = 0x00
        self.stopPacket[4] = 0x00
        self.stopPacket[5] = 0x00
        self.stopPacket[6] = 0x28
        self.stopPacket[7] = 0xEA
        self.stopPacket[8] = 0x84
        self.stopPacket[9] = 0xEE

        self.startFilterPacket[0] = 0xF5
        self.startFilterPacket[1] = 0xD9
        self.startFilterPacket[2] = 0x01
        self.startFilterPacket[3] = 0x00
        self.startFilterPacket[4] = 0x00
        self.startFilterPacket[5] = 0x00
        self.startFilterPacket[6] = 0xB7
        self.startFilterPacket[7] = 0x1F
        self.startFilterPacket[8] = 0xBA
        self.startFilterPacket[9] = 0xBA

        self.stopFilterPacket[0] = 0xF5
        self.stopFilterPacket[1] = 0xD9
        self.stopFilterPacket[2] = 0x00
        self.stopFilterPacket[3] = 0x00
        self.stopFilterPacket[4] = 0x00
        self.stopFilterPacket[5] = 0x00
        self.stopFilterPacket[6] = 0x00
        self.stopFilterPacket[7] = 0x85
        self.stopFilterPacket[8] = 0xD7
        self.stopFilterPacket[9] = 0x66

        self.setFreqPacket[0] = 0xF5
        self.setFreqPacket[1] = 0xE2
        self.setFreqPacket[2] = 0x00
        self.setFreqPacket[3] = 0x00
        self.setFreqPacket[4] = 0x00
        self.setFreqPacket[5] = 0x00
        self.setFreqPacket[6] = 0x00
        self.setFreqPacket[7] = 0x00
        self.setFreqPacket[8] = 0x00
        self.setFreqPacket[9] = 0x00

    def readPacket(self,size):
        packet = bytearray(size)
        firstData = 0xFA
        packet[0]=firstData
        for i in range(size-1):
            buff = self.i2c.readfrom(LIDAR_ADDR,size)
        for i in buff:
            print(buff[i])

        return packet

    def startFilter(self):
        self.i2c.writeto(LIDAR_ADDR,self.startFilterPacket)
        pyb.delay(20)
        print('Filter Started')

    def setMeasureMode(self):
        self.i2c.writeto(LIDAR_ADDR,self.setModePacket)
        pyb.delay(20)
        print('Measure Mode set to single measurement')

    def startMeasure(self):
        self.i2c.writeto(LIDAR_ADDR,self.startPacket)
        pyb.delay(20)
        print('Measurement Started')

    def getValue(self):
        buff = self.readPacket(24)
        self.distance = buff[4] | buff[5] << 8
        self.amplitude = buff[8] | buff[9] << 8




lidar = Lidar07()
while lidar.i2c.scan() == []:
    print('Waiting')
    pyb.delay(500)
print (lidar.i2c.scan())
lidar.begin()
lidar.startFilter()
lidar.setMeasureMode()
pyb.delay(2000)

while(True):
    lidar.startMeasure()
    lidar.getValue()
    print("Distance: ")
    print(lidar.distance)
    print("Amplitude: ")
    print(lidar.amplitude)
    print("\n")
    pyb.delay(1000)
