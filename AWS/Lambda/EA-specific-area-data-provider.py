import json
import boto3
from custom_encoder import CustomEncoder

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table("EA-Area-Wise-Things-Data")


def lambda_handler(event, context):
    
    areaUID = event['queryStringParameters']['areaUID']
    areaInfo = table.get_item(Key={"areaUID": areaUID})["Item"]
    
    return buildResponse(200, areaInfo)
    
def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)

    return response
