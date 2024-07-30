import json
import boto3
import http.client

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table("EA-Area-Wise-Things-Data")
s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    response = table.scan()["Items"]
    bucket_name = 'ea-area-wise-satellite-imgs'
    
    for area in response:
        areaDetails = area["details"]
        object_key = area["areaUID"]+".png"
        lat = areaDetails['lat']
        lng = areaDetails['lng']
        
        params = {
            "center": f"{lat},{lng}",
            "zoom": "14",
            "size": "400x400",
            "maptype": "satellite",
            "key": "GOOGLE_MAPS_API_KEY"
        }
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        url = f"/maps/api/staticmap?{query_string}"
        
        conn = http.client.HTTPSConnection("maps.googleapis.com")
        conn.request("GET", url)
        response = conn.getresponse()
        
        if response.status == 200:
            image_data = response.read()
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=image_data, ContentType='image/png')
        
    
    return {
        'statusCode': 200,
        'body': json.dumps('Satellite imgs updated')
    }
