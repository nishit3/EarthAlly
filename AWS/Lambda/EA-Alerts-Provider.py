import json
import boto3

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table("EA-Alerts")

def lambda_handler(event, context):
    
    alerts = table.scan()["Items"]
    toBeReturned = []
    
    try:
        areaUID = event['queryStringParameters']['areaUID']
        for alert in alerts:
            if alert['areaUID'] == areaUID:
                toBeReturned.append(alert)
    except:
        toBeReturned = alerts
        
    
    return {
        'statusCode': 200,
        'headers':{
            'content-type': 'application/json'
        },
        'body': json.dumps({"alerts": toBeReturned})
    }
