import json
import boto3
import http.client
from decimal import Decimal

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table("EA-Area-Wise-Things-Data")
alertTable = dynamoDB.Table("EA-Alerts")

def lambda_handler(event, context):
    
    reqBody = json.loads(event['body'])
    
    moisture = Decimal(str(reqBody['moisture']))
    
    areaUID = reqBody['areaUID']
    moduleID = reqBody['moduleID']
    
    table.update_item(
        Key={
            'areaUID': areaUID
        },
        UpdateExpression=f'SET #a.#b.#c = :a',
        ExpressionAttributeValues={
            ':a': moisture,
        },
        ExpressionAttributeNames={
            '#a': 'soil_modules',
            '#b': moduleID,
            '#c': 'moisture',
        },
        ReturnValues='ALL_NEW'
    )
    
    
    api_url = "worldtimeapi.org"
    path = "/api/timezone/Asia/Kolkata"
    conn = http.client.HTTPSConnection(api_url)
    conn.request("GET", path)
    response = conn.getresponse()
    response_data = response.read().decode("utf-8")
    date_day_data = json.loads(response_data)
    dateTime = date_day_data["datetime"]
    timeStartI = dateTime.find('T')+1
    timeEndI = dateTime.find('.')
    todaysDate = dateTime[0:10]
    todaysDate = str(todaysDate[-2])+str(todaysDate[-1])+'-'+str(todaysDate[5])+str(todaysDate[6])+'-'+str(todaysDate[0:4])
    todaysTime = dateTime[timeStartI : timeEndI]
    
    areaInfo = table.get_item(Key={'areaUID': areaUID})["Item"]
    wind_speed = areaInfo['wind_speed']
    areaAddress = areaInfo['details']['address']
    moduleAddress = areaInfo['soil_modules'][moduleID]['address']
    
    if wind_speed >= 4.00 and moisture <= 20:
        alertTable.put_item(
            Item = {
                "alertUID": "S"+todaysDate+todaysTime+areaUID,
                "areaUID": areaUID,
                "DateTime": todaysDate+' '+todaysTime,
                "Message": 'Dust storm is highly possible in '+moduleAddress+', '+areaAddress
            }
        )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('UPDATED')
    }
