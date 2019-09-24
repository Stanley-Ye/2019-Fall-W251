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
    vsi_broker.publish("cloudimage", payload=msg.payload)
    print("Message received and sent to VSI.")
    

# VSI
vsi_broker_address = "169.44.183.162"
vsi_broker = mqtt.Client("vsi")
try:
    vsi_broker.connect(vsi_broker_address)
except:
    print("FAILED to connect to VSI")
else:
    print("SUCCEEDED to connect to VSI")

# Jetson
client_address = "172.18.0.2"
client = mqtt.Client("forwarder")
client.on_connect = on_connect
client.on_message = on_message
try:
    client.connect(client_address)
except:
    print("FAILED to connect to Jetson")
else:
    print("SUCCEEDED to connect to Jetson")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
