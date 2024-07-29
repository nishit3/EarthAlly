import json
import boto3
from decimal import Decimal

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table("EA-Area-Wise-Things-Data")
alertTable = dynamoDB.Table("EA-Alerts")
client = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    
    reqBody = json.loads(event['body'])
    
    pH = Decimal(str(reqBody['pH']))
    turbidity = Decimal(str(reqBody['turbidity']))
    TDS = Decimal(str(reqBody['TDS']))
    
    areaUID = reqBody['areaUID']
    moduleID = reqBody['moduleID']
    
    areaDetails = table.get_item(Key={'areaUID': areaUID})["Item"]
    moduleAddress = areaDetails['water_modules'][moduleID]['address']
    areaAddress = areaDetails['details']['address']
    
    table.update_item(
            Key={
                'areaUID': areaUID
            },
            UpdateExpression=f'SET #a.#b.#c = :a, #a.#b.#d = :b, #a.#b.#e = :c',
            ExpressionAttributeValues={
                ':a': pH,
                ':b': turbidity,
                ':c': TDS,
            },
            ExpressionAttributeNames={
                '#a': 'water_modules',
                '#b': moduleID,
                '#c': 'pH',
                '#d': 'turbidity',
                '#e': 'TDS',
            },
            ReturnValues='ALL_NEW'
        )
        
    response = client.invoke_endpoint(
        EndpointName='pytorch-inference-2024-07-28-16-30-18-875', 
        ContentType='application/json',
        Body=json.dumps({
            "pH": float(str(pH)), 
            "TDS": float(str(TDS)), 
            "turbidity": float(str(turbidity))}
            )
    )
    response_body = response['Body']
    body_string = response_body.read().decode('utf-8')
    isGood = json.loads(body_string)['isGood']
    
    if isGood == 0:
        alertTable.put_item(
            Item = {
                "alertUID": "W"+todaysDate+todaysTime+areaUID,
                "areaUID": areaUID,
                "DateTime": todaysDate+' '+todaysTime,
                "Message": 'Water quality is bad in '+moduleAddress+' '+areaAddress
            }
        )
        
    
    return {
        'statusCode': 200,
        'body': json.dumps('UPDATED')
    }
