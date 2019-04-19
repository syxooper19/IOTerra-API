#!/usr/bin/env python
#

#import pour humidite / temperature
import grovepi
import math

#import pour luminosite
import time

#import pour firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


#date courante
import datetime
now = datetime.datetime.now()



# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'ioterra',
})

db = firestore.client()


# Lecture données Firestore
#users_ref = db.collection(u'Terrarium').document('KreKAs5CarjyWiko68bv').collection(u'Mesures')
#docs = users_ref.get()

#for doc in docs:
#    print(u'{} => {}'.format(doc.id, doc.to_dict()))





# Connecter le capteur de lumiere au port A0
light_sensor = 0
grovepi.pinMode(light_sensor,"INPUT")

# Connexion du capteur humidite temperature sur le port D4
sensor = 4

# temp_humidity_sensor_type
# Utilisation du capteur "bleu"
blue = 0    
white = 1


try:
    [temp,humidity] = grovepi.dht(sensor,blue)  
    sensor_value = grovepi.analogRead(light_sensor)


   
    if math.isnan(temp) == False and math.isnan(humidity) == False and math.isnan(sensor_value) == False:
        print("temperature = %.02f C hygrométrie =%.02f%%"%(temp, humidity))
        print("luminosité = %d" %(sensor_value))


        data = {
            u'temperature': temp,
            u'hygrometrie': humidity,
            u'luminosite':sensor_value,
            'date':now        
        }

        # Add a new doc in collection 'cities' with ID 'LA'
        db.collection(u'Terrarium').document('KreKAs5CarjyWiko68bv').collection(u'Mesures').document().set(data)

except IOError:
    print ("Error")
