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
        
    toBeReturned = []
    for area in result:
        basicDetails = {}
        basicDetails["areaUID"] = area["areaUID"]
        basicDetails["name"] = area["details"]["name"]
        basicDetails["address"] = area["details"]["address"]
        basicDetails["lat"] = area["details"]["lat"]
        basicDetails["lng"] = area["details"]["lng"]
        toBeReturned.append(basicDetails)
        
    body = {
        "areasBasicInformation": toBeReturned
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
