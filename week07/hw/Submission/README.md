### Questions
* Describe your solution in detail.  What neural network did you use? What dataset was it trained on? What accuracy does it achieve?
  - For face detection, I used the Multi-task Cascade CNN (MTCNN) with the pre-trained model.  According to this [article](https://blog.datawow.io/face-detection-haar-cascade-vs-mtcnn-13af4aa180e6), MTCNN achieves 98% accuracy in face detection, compared to 95% for OpenCV.
* Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?
  - During my testing, MTCNN achieved high accuracy and appears to be a robust, production-grade system.
* What framerate does this method achieve on the Jetson? Where is the bottleneck?
  - On the Jetson TX2, MTCNN is much slower (3 FPS) than OpenCV (30 FPS).  Bottleneck is due to MTCNN's more complex and accurate DL model, compared to OpenCV.
* Which is a better quality detector: the OpenCV or yours?
  - MTCNN is better quality than OpenCV, at the tradeoff of speed, i.e., FPS.


### Turn-In
* Code related to the neural face detector
  - face_detector.py
* Object storage for detected face images
  - [link](https://cloud.ibm.com/objectstorage/crn%3Av1%3Abluemix%3Apublic%3Acloud-object-storage%3Aglobal%3Aa%2Fd037c9645257443e814577efd4ed2d9f%3A1c5500be-176d-4e6c-a4bb-ff0bc3f07a2a%3A%3A?bucket=sye2&bucketRegion=us-east&endpoint=s3.us-east.cloud-object-storage.appdomain.cloud&paneId=bucket_overview)


### Jetson TX2 ###
* Create Docker images
  - sudo docker build -f Dockerfile.msqtt_broker -t msqtt_broker .
  - sudo docker build -f Dockerfile.msqtt_forwarder -t msqtt_forwarder .
  - sudo docker pull w251/tensorrtlab05:dev-tx2-4.2.1_b97

* Create network bridge
  - sudo docker network create --driver bridge hw03

* Create container: broker
  - sudo docker run --name broker --network hw03 -p 1883:1883 msqtt_broker

* Create container: forwarder
  - sudo docker run --name forwarder --network hw03 -ti msqtt_forwarder sh
  - python3 forwarder.py

* Create container: detector
  - sudo docker run --name detector --network hw03 --device=/dev/video1:/dev/video1 -ti w251/tensorrtlab05:dev-tx2-4.2.1_b97 bash
  - python3 face_detector.py


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
