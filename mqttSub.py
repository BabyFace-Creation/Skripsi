import random
import time

from paho.mqtt import client as mqtt_client

broker = 'armadillo.rmq.cloudamqp.com'
port = 1883
topic = "jmlPelanggan"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'zwlrpnko:zwlrpnko'
password = 'VhM5RTgFuKVMudvzrAoRZk5ebITarytH'
msg = 0

class Subscribe:
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        print(msg)
        

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.connect(broker, port)
    client.loop_start()
    client.subscribe(topic)
    client.on_message=on_message

    time.sleep(30)
    client.loop_stop()

    def passData():
        print(msg)
        return msg
