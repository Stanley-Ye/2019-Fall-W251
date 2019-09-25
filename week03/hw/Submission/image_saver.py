# Object Storage
# Copy from IBM Cloud account
credentials = {
  "apikey": "-LGCqqvSwnTn1c9dKM6en_BgxAuW7Sqr6rn_ieHvHYqA",
  "cos_hmac_keys": {
    "access_key_id": "f7094ac9c312427ea5987dcb805faf2a",
    "secret_access_key": "c405412de352f94e8d9559f87b93a824fa02772850fe0489"
  },
  "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
  "iam_apikey_description": "Auto-generated for key f7094ac9-c312-427e-a598-7dcb805faf2a",
  "iam_apikey_name": "Service credentials-1",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/d037c9645257443e814577efd4ed2d9f::serviceid:ServiceId-38816ce8-30ce-4803-b1f0-f8a99e8b9e81",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/d037c9645257443e814577efd4ed2d9f:1c5500be-176d-4e6c-a4bb-ff0bc3f07a2a::"
}


# References:
# - https://cloud.ibm.com/docs/services/cloud-object-storage/libraries?topic=cloud-object-storage-python
# - https://dataplatform.cloud.ibm.com/analytics/notebooks/v2/ee1d0b44-0fce-4cf6-8545-e1dc961d0668/view?access_token=c0489b861ab65f63be7e3c5ce962003a2a0197660e67ecb140c477c2e11b5fe3
from ibm_botocore.client import Config, ClientError
import ibm_boto3

cos = ibm_boto3.resource("s3",
                         ibm_api_key_id='-LGCqqvSwnTn1c9dKM6en_BgxAuW7Sqr6rn_ieHvHYqA',
                         ibm_service_instance_id='crn:v1:bluemix:public:cloud-object-storage:global:a/d037c9645257443e814577efd4ed2d9f:1c5500be-176d-4e6c-a4bb-ff0bc3f07a2a::',
                         ibm_auth_endpoint='https://iam.cloud.ibm.com/identity/token',
                         config=Config(signature_version="oauth"),
                         endpoint_url='https://s3.us-east.cloud-object-storage.appdomain.cloud')


import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    topic = "cloudimage"
    client.subscribe(topic=topic, qos=1)
    print("Subscribed: %s" %(topic))

# The callback for when a PUBLISH message is received from the server.
count = 1
def on_message(client, userdata, msg):
    print("Message received")
    global count, cos
    print("BB0")
    bucket = "sye2"
    print("BB1")
    object = "image_" + str(count) + ".png"
    print("BB2")
    count = count + 1
    print("BF0")
    try:
        print("BF1")
        #print(msg.payload)
        #cos.put_object(Bucket=bucket, Key=object, Body=msg.payload)
        cos.Bucket(name=bucket).put_object(Key=object, Body=msg.payload)
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create bucket: {0}".format(e))
        

    #except ClientError as e:
    #    error_code = e.response['Error']['Code']
    #    print("ERROR: %s" %(error_code))
    print("AF")
        
    print("Saved (%s) to bucket (%s)" %(object, bucket))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")

    
# Connect to broker (VSI)
client = mqtt.Client("vsi_broker")
client_address = "172.19.0.2"
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(client_address)
print("SUCCEEDED to connect to VSI")


client.loop_forever()

