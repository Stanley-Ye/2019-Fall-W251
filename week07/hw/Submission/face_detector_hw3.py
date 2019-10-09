import numpy as np
import cv2
import paho.mqtt.client as mqtt
import os.path
from os import path
import time

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
    start = time.time()
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    end = time.time()
    frames_per_second = 1 / (end - start)
    print("FPS: %f" %(frames_per_second))
    
    for (x,y,w,h) in faces:
        # Reference code: https://docs.opencv.org/3.4.1/d7/d8b/tutorial_py_face_detection.html
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = frame[y:y+h, x:x+w]
        rc,png = cv2.imencode('.png', roi_gray)
        msg = png.tobytes()

        # Publish msg
        client.publish(topic, payload=msg)
        #print("Image published: %i" %(counter))
        counter = counter + 1
    time.sleep(1)

        
# Conclude
cap.release()
cv2.destroyAllWindows()
