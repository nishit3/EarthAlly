import json
import http.client
import boto3
import base64

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
    
    areaCamInfo = key.replace(".jpeg", "")
    endI = areaCamInfo.find("c")
    areaUID = areaCamInfo[0:endI]
    areaInfo = table.get_item(Key={"areaUID": areaUID})["Item"]
    camAddress = areaInfo['cam_modules'][areaCamInfo]
    
    
    
    # Ngrok
    post_url = "5365-2402-a00-405-9ebe-ad72-3991-28ed-2437.ngrok-free.app"
    post_path = "/detectGarbage"
    post_conn = http.client.HTTPSConnection(post_url)
    headers = {
        'Content-Type': 'application/json',
    }
    post_conn.request("POST", post_path, reqBody, headers)
    post_response = post_conn.getresponse()
    post_response_data = post_response.read().decode("utf-8")
    post_conn.close()
    prediction = json.loads(post_response_data)['prediction']
    if prediction != 'Clean Road':
        alertTable.put_item(
            Item = {
                "alertUID": "G"+todaysDate+todaysTime+areaCamInfo,
                "areaUID": areaUID,
                "DateTime": todaysDate+' '+todaysTime,
                "Message": 'Excessive '+prediction+' detected in '+camAddress
            }
        )
        
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('New Satellite Img Processed')
    }
