import json
import http.client
import boto3
import base64
from decimal import Decimal

s3_client = boto3.client('s3')
dynamoDB = boto3.resource('dynamodb')

table = dynamoDB.Table("EA-Area-Wise-Things-Data")
alertTable = dynamoDB.Table("EA-Alerts")

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    response = s3_client.get_object(Bucket=bucket, Key=key)
    image_data = response['Body'].read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    reqBody = json.dumps({"b64EncodedImgString": encoded_image})
    
    
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
    

    areaUID = key.replace(".png", "")
    areaDetail = table.get_item(Key={'areaUID': areaUID})["Item"]
    prevDeforestationIndex = areaDetail["deforestation_index"]
    address = areaDetail['details']['address']
    
    
    
    # Ngrok
    post_url = "2817-2402-a00-405-9ebe-ad72-3991-28ed-2437.ngrok-free.app"
    
    
    
    # Deforestation
    post_path = "/detectDeforestation"
    post_conn = http.client.HTTPSConnection(post_url)
    headers = {
        'Content-Type': 'application/json',
    }
    post_conn.request("POST", post_path, reqBody, headers)
    post_response = post_conn.getresponse()
    post_response_data = post_response.read().decode("utf-8")
    post_conn.close()
    pred = json.loads(post_response_data)['prediction']
    prediction = Decimal(str(pred)) 
    if ((prediction - prevDeforestationIndex)/prevDeforestationIndex)*100 > 50.00:
        alertTable.put_item(
            Item = {
                "alertUID": "D"+todaysDate+todaysTime+areaUID,
                "areaUID": areaUID,
                "DateTime": todaysDate+' '+todaysTime,
                "Message": 'Chances of deforestation are high in '+address
            }
        )
    table.update_item(
        Key={
            'areaUID': areaUID
        },
        UpdateExpression=f'SET #a = :a',
        ExpressionAttributeValues={
            ':a': prediction,
        },
        ExpressionAttributeNames={
            '#a': 'deforestation_index',
        },
        ReturnValues='ALL_NEW'
    )
    
    
    # WildFire
    post_path = "/detectWildFire"
    post_conn = http.client.HTTPSConnection(post_url)
    headers = {
        'Content-Type': 'application/json',
    }
    post_conn.request("POST", post_path, reqBody, headers)
    post_response = post_conn.getresponse()
    post_response_data = post_response.read().decode("utf-8")
    post_conn.close()
    prediction = json.loads(post_response_data)['prediction']
    if prediction == 'wildfire':
        alertTable.put_item(
            Item = {
                "alertUID": "WF"+todaysDate+todaysTime+areaUID,
                "areaUID": areaUID,
                "DateTime": todaysDate+' '+todaysTime,
                "Message": 'Chances of wildfire are high in '+address
            }
        )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('New Satellite Img Processed')
    }
