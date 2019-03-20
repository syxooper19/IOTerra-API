#!/usr/bin/env python
#
import grovepi
import math

# Connexion du capteur humidite temperature sur le port D4
sensor = 4

# temp_humidity_sensor_type
# Utilisation du capteur "bleu"
blue = 0    
white = 1


try:
    [temp,humidity] = grovepi.dht(sensor,blue)  
    if math.isnan(temp) == False and math.isnan(humidity) == False:
        print("temperature = %.02f C hygrométrie =%.02f%%"%(temp, humidity))

except IOError:
    print ("Error")
