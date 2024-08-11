import json
import http.client
import boto3
from decimal import Decimal

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table("EA-Area-Wise-Things-Data")

def lambda_handler(event, context):
    
    api_url = "weather.visualcrossing.com"
    
    response = table.scan()["Items"]
    for area in response:
        areaDetails = area["details"]
        areaUID = area["areaUID"]
        lat = areaDetails['lat']
        lng = areaDetails['lng']
        path = f"/VisualCrossingWebServices/rest/services/timeline/{lat},{lng}?iconSet=icons2&key=KEY"
        conn = http.client.HTTPSConnection(api_url)
        conn.request("GET", path)
        response = conn.getresponse()
        response_data = response.read().decode("utf-8")
        responseBody = json.loads(response_data)['currentConditions']
        
        wind_speed = Decimal(str(responseBody['windspeed']))
        weather_condition = responseBody['icon']
        
        table.update_item(
            Key={
                'areaUID': areaUID
            },
            UpdateExpression=f'SET #a = :a, #b = :b',
            ExpressionAttributeValues={
                ':a': weather_condition,
                ':b': wind_speed,
            },
            ExpressionAttributeNames={
                '#a': 'weather_condition',
                '#b': 'wind_speed',
            },
            ReturnValues='ALL_NEW'
        )
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
