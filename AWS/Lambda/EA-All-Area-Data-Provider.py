import json
import boto3

from custom_encoder import CustomEncoder

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table("EA-Area-Wise-Things-Data")


def lambda_handler(event, context):
    
    response = table.scan()
    result = response["Items"]
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        result.extend(response['Items'])

    body = {
        "areaWiseData": result
    }
    return buildResponse(200, body)
    
    
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
