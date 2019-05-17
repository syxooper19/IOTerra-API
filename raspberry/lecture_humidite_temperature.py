#!/usr/bin/env python
#

# infos mail
import conf

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

#import pour l'envoi de mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def detecteProbleme(hygroMesure, tempMesure):
    paramTerra  = db.collection(u'Terrarium').document('KreKAs5CarjyWiko68bv')
    doc         = paramTerra.get()
    adresseMail = doc.to_dict().get('AlertesSouhaitee')

    if (adresseMail != ""):
        hygrometrie     =   doc.to_dict().get('HygrométrieSouhaitee')
        temperature     =   doc.to_dict().get('temperatureSouhaitee')
        toleranceHygro  =   doc.to_dict().get('toleranceHygro')
        toleranceTemp   =   doc.to_dict().get('toleranceTemp')
        
        #Si l'hygrométrie est non conforme
        if (float(hygroMesure) < float(hygrometrie)*(1+float(toleranceHygro)/100)) & (float(hygroMesure) > float(hygrometrie)*(1-float(toleranceHygro)/100)):
            print('hygrometrie conforme')
        else:
            ecart       =   float(hygroMesure) - float(hygrometrie);
            envoi_mail(adresseMail, 'hygrométrie', ecart)
            
        
        #Si la température est non conforme
        if (float(tempMesure) < float(temperature)*(1+float(toleranceTemp)/100)) & (float(tempMesure) > float(temperature)*(1-float(toleranceTemp)/100)):
            print('temperature conforme')
        else:
            ecart       =   float(tempMesure) - float(temperature);
            envoi_mail(adresseMail, 'température', ecart)
           


# Permet d'envoyer un email
def envoi_mail(mail, hygroOuTemp, ecart):

    if (hygroOuTemp == 'température'):
        uniteMesure =   '°C'
    else:
        uniteMesure =   '%'

    msg = MIMEMultipart()
    msg['From'] = conf.adrFrom
    msg['To'] = mail
    msg['Subject'] = 'IOTerra - Alerte ' + hygroOuTemp
    message = 'Bonjour. Une anomalie à été détectée sur votre terrarium : un écart de ' + str(ecart) + uniteMesure

    msg.attach(MIMEText(message))
    
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(conf.adrFrom, conf.mdpMail)
    mailserver.sendmail(conf.adrFrom, mail, msg.as_string())
    mailserver.quit()
    
    
    
    

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
        #db.collection(u'Terrarium').document('KreKAs5CarjyWiko68bv').collection(u'Mesures').document().set(data)
        detecteProbleme(humidity, temp)
        
except IOError:
    print ("Error")
