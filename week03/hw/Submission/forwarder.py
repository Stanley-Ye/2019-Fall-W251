# Reference: https://pypi.org/project/paho-mqtt/

import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("image")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    vsi_broker.publish("image", msg.payload)
    

# VSI
vsi_broker_address = "169.44.183.162"
vsi_broker = mqtt.Client("vsi")
try:
    vsi_broker.connect(vsi_broker_address, 1883)
except:
    print("FAILED to connect to VSI")

# Jetson
client_address = "192.168.1.18"
client = mqtt.Client("jetson")
client.on_connect = on_connect
client.on_message = on_message
try:
    client.connect(client_address, 1883)
except:
    print("FAILED to connect to Jetson")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
