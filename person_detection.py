# Untitled - By: arw_2 - Sun Mar 26 2023

import sensor, image, time, os, tf, pyb

person_threshold = 0.65

led = pyb.LED(1)
led.off()

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

net = tf.load('person_detection.tflite', True)
labels = ['unsure', 'person', 'no_person']

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
        img.draw_rectangle(obj.rect())
        img.draw_string(obj.x()+3, obj.y()-1, labels[obj.output().index(max(obj.output()))], mono_space=False)

        # Light LED if person detected
        idx = labels.index('person')
        if obj.output()[idx] > person_threshold:
            led.on()
        else:
            led.off()


    print(clock.fps(), "fps")
