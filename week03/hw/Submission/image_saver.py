# Object Storage
# Copy from IBM Cloud account
credentials = {
  "apikey": "xBX1K4-FdKQB7_MuWWUgMS-l9qzMTlkjO9F9WiLl6sze",
  "cos_hmac_keys": {
    "access_key_id": "9af8829fd7a44419a85d18d5ef542d56",
    "secret_access_key": "72faa530caae018e7d3e834c1d27004f48a0c95de805ccb0"
  },
  "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
  "iam_apikey_description": "Auto-generated for key 9af8829f-d7a4-4419-a85d-18d5ef542d56",
  "iam_apikey_name": "Service credentials-1",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/d037c9645257443e814577efd4ed2d9f::serviceid:ServiceId-06a1eaa2-db6e-4ae1-b9a7-9b72c262cd9e",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/d037c9645257443e814577efd4ed2d9f:b10bdac1-9c74-48d7-a520-98d2d4d54fab::"
}


# Reference: https://cloud.ibm.com/docs/services/cloud-object-storage/libraries?topic=cloud-object-storage-python
import ibm_boto3
from ibm_botocore.client import Config, ClientError

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=credentials['apikey'],
    ibm_service_instance_id=credentials['resource_instance_id'],
    ibm_auth_endpoint='https://iam.bluemix.net/oidc/token',
    config=Config(signature_version="oauth"),
    endpoint_url='https://ss3.sjc04.cloud-object-storage.appdomain.cloud'
)




import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("image")

# The callback for when a PUBLISH message is received from the server.
count = 1
def on_message(client, userdata, msg):
    global count
    bucket = 'sye-w251-hw3'
    object = "image_" + count
    count = count + 1
    cos.put_object(
        Bucket=bucket,
        Key=object,
        Body=msg.payload
    )
    print("Saved (%s) to bucket (%s)" %(object, bucket))

    
# Connect to broker (VSI)
try:
    client = mqtt.Client("vsi")
    client_address = "172.19.0.2"
    client.connect(client_address)
except:
    print("FAILED to connect to VSI")
else:
    print("SUCCEEDED to connect to VSI")



client.loop_forever()

