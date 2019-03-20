#!/usr/bin/env python
#

import time
import grovepi

# Connecter le capteur de lumiere au port A0
light_sensor = 0



grovepi.pinMode(light_sensor,"INPUT")

try:
    # Get sensor value
    sensor_value = grovepi.analogRead(light_sensor)

    print("luminosité = %d" %(sensor_value))


except IOError:
    print ("Error")
