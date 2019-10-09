import numpy as np
import cv2
import paho.mqtt.client as mqtt
import os.path
from os import path
import time

from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN

# create the detector, using default weights
detector = MTCNN()

# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
cap = cv2.VideoCapture(1)

# Init
xml = '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml'
if not path.exists(xml):
    xml = 'haarcascade_frontalface_default.xml'
if not path.exists(xml):
    print("FILE NOT FOUND: haarcascade_frontalface_default.xml")
    exit()

face_cascade = cv2.CascadeClassifier(xml)
topic = "image"
counter = 0
prev_counter = -1
num_images = 20


def on_publish(client, msg, rc):
    print("Image published")


# Connect to broker
client = mqtt.Client("jetson")
client_address = "172.18.0.2"
client.on_publish = on_publish
client.connect(client_address)
print("SUCCEEDED to connect to Jetson")
    
# Capture images
while(counter < num_images):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if counter != prev_counter:
        print("Image captured: %i" %(counter))
        prev_counter = counter

    # We don't use the color information, so might as well save space
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # face detection and other logic goes here
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Show frame
    #pyplot.imshow(frame)
    
    # Use MTCNN to detect faces
    result_list = detector.detect_faces(frame)
    
    # Publish faces to MQTT
    for i in range(len(result_list)):
        # Get confidence
        conf = result_list[i]['confidence']
        print("CONF=%f" %(conf))
        print(result_list[i])

        # get coordinates
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
        face = frame[y1:y2, x1:x2]
        rc,png = cv2.imencode('.png', face)
        msg = png.tobytes()
   
        # Publish msg
        client.publish(topic, payload=msg)
        print("Image published: %i" %(counter))
        counter = counter + 1
        
    time.sleep(1)

        
# Conclude
cap.release()
cv2.destroyAllWindows()
