import random
import time

import paho.mqtt.client as mqttClient

broker = 'armadillo.rmq.cloudamqp.com'
port = 1883
topic = "jmlPelanggan"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'zwlrpnko:zwlrpnko'
password = 'VhM5RTgFuKVMudvzrAoRZk5ebITarytH'
value = 0


client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(username, password=password)    #set username and password
                    #attach function to callback
client.connect(broker, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
try:
    while True:
 
        value = input('Enter the message:')
        client.publish("python/test",value)
 
except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()