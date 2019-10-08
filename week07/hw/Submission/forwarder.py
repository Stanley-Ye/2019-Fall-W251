# References:
# - https://pypi.org/project/paho-mqtt/
# - https://www.eclipse.org/paho/clients/python/docs/

import paho.mqtt.client as mqtt

topic1 = "image"
topic2 = "cloudimage"

# The callback for when the client receives a CONNACK response from the server.
def on_connect1(client, userdata, flags, rc):
    global topic1
    print("Connected1 with result code "+str(rc))
    client.subscribe(topic1)

def on_connect2(client, userdata, flags, rc):
    global topic2
    print("Connected2 with result code "+str(rc))
    client.subscribe(topic=topic2, qos=1)

# The callback for when a PUBLISH message is received from the server.
def on_message1(client, userdata, msg):
    print("Message received1")
    global vsi_broker, topic2
    rc = vsi_broker.publish(topic=topic2, payload=msg.payload, qos=1, retain=False)
    print("vsi_broker.publish: %s" %(rc))

def on_message2(client, userdata, msg):
    print("Message received2")

def on_publish1(client, userdata, mid):
    print("Message published1")
    
def on_publish2(client, userdata, mid):
    print("Message published2: ")
    

# VSI
vsi_broker_address = "169.44.183.162"
vsi_broker = mqtt.Client("vsi")
vsi_broker.on_connect = on_connect2
vsi_broker.on_publish = on_publish2
vsi_broker.on_message = on_message2
vsi_broker.connect(vsi_broker_address)
print("SUCCEEDED to connect to VSI")

# Jetson
jetson_address = "172.18.0.4"
jetson = mqtt.Client("forwarder")
jetson.on_connect = on_connect1
jetson.on_message = on_message1
jetson.on_publish = on_publish1
jetson.connect(jetson_address)
print("SUCCEEDED to connect to Jetson")

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
jetson.loop_forever()
