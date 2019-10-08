### Jetson TX2 ###
* Create Docker images
  - sudo docker build -f Dockerfile.msqtt_broker -t msqtt_broker .
  - sudo docker build -f Dockerfile.msqtt_forwarder -t msqtt_forwarder .
  - sudo docker build -f Dockerfile.face_detector -t face_detector .

* Create network bridge
  - sudo docker network create --driver bridge hw03

* Create container: broker
  - sudo docker run --name broker --network hw03 -p 1883:1883 msqtt_broker

* Create container: forwarder
  - #Assumes IP of broker is 172.18.0.4
  - sudo docker run --name forwarder --network hw03 -ti msqtt_forwarder sh
  - python3 forwarder.py

* Create container: detector
  - #Assumes IP of broker is 172.18.0.4
  - sudo docker run --name detector --network hw03 --device=/dev/video1:/dev/video1 -ti face_detector bash
  - python face_detector.py


### VSI ###
* Create Docker images
  - sudo docker build -f Dockerfile.msqtt_broker -t msqtt_broker .
  - sudo docker build -f Dockerfile.image_saver -t image_saver .

* Create network bridge
  - sudo docker network create --driver bridge hw03

* Create container: broker
  - sudo docker run --name broker --network hw03 -p 1883:1883 msqtt_broker

* Create container: image_saver
  - sudo docker run --name image_saver --network hw03 -ti image_saver bash
  - python3 image_saver.py
