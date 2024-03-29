# File:          classify.py
# Description:   This script holds everything necessary to classify an object.
# Authors:       C. Jackson, J. Markle, C. McCarver, A. Mendoza, A. White, H. Williams
# Date Created:  3/3/2023
# Last Modified: 3/3/2023

import sensor, image, time, os, tf, pyb

person_threshold = 0.9

led = pyb.LED(1)
led.off()

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

net = tf.load('SED-model.tflite')
labels = ['nothing', 'car', 'person']

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    for obj in net.classify(img, min_scale=1.0, scale_mul=0.5, x_overlap=0.0, y_overlap=0.0):

        # Give classification scores
        print("***********\nDetections at [x=%d, y=%d, w=%d, h=%d]" % obj.rect())
        for i in range(len(obj.output())):
            print("%s = %f" % (labels[i], obj.output()[i]))

        # Highlight identified object
        img.draw_rectangle(obj.rect(), color=[0,0,0])
        final_label = labels[obj.output().index(max(obj.output()))]
        idx = labels.index(final_label)
        if obj.output()[idx] < person_threshold:
            final_label = 'nothing'

        img.draw_string(obj.x()+3, obj.y()-1, final_label, color=[0,0,0], mono_space=False)

        # Light LED if person detected
        idx = labels.index('person')
        if obj.output()[idx] > person_threshold:
            led.on()
        else:
            led.off()


    print(clock.fps(), "fps")
    print(net.ram())

