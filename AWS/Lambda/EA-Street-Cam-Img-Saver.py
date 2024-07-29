import json
import base64
import boto3
from io import BytesIO
import datetime

client=boto3.client('s3')

def decode(encoded_string):
  decoded_bytes = base64.b64decode(encoded_string)
  decoded_string = decoded_bytes.decode('ascii')
  return decoded_string
  
  
def lambda_handler(event, context):
    
    camUID = event['queryStringParameters']['camUID']

    encodedImageString = event['body']
    binaryData = base64.b64decode(encodedImageString)
    
    response = client.put_object(
    Body=binaryData,
    Bucket='ea-street-cam-imgs',
    Key=camUID+'.jpeg',
    ContentType='image/jpeg',
    )
    
    return {
        'statusCode': 200,
        'headers': {
            'allow-access-control-origin': '*'
        },
        'body': json.dumps('SUCCESS')
    }
