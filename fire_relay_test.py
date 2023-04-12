# File:          fire_relay_test.py
# Description:   This script holds the functions used to demonstrate firing a relay when the
#                OpenMV classifies correctly.
# Authors:       C. Jackson, J. Markle, C. McCarver, A. Mendoza, A. White, H. Williams
# Date Created:  4/12/2023
# Last Modified: 4/12/2023

import sensor, image, time, pyb

from pyb import Pin

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

fire_relay = Pin("P0", Pin.OUT_PP)

fire_relay.high()

fire_relay.low()
