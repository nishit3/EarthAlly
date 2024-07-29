import json
import boto3
from decimal import Decimal

dynamoDB = boto3.resource('dynamodb')
table = dynamoDB.Table("EA-Area-Wise-Things-Data")
client = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    
    reqBody = json.loads(event['body'])
    
    AQI = reqBody["AQI"]
    significant_pollutant = reqBody["significant_pollutant"]
    CO = Decimal(str(reqBody["CO"]))
    humd = Decimal(str(reqBody["humd"]))
    NH3 = Decimal(str(reqBody["NH3"]))
    NO2 = Decimal(str(reqBody["NO2"]))
    O3 = Decimal(str(reqBody["O3"]))
    PM10 = Decimal(str(reqBody["PM10"]))
    PM25 = Decimal(str(reqBody["PM2.5"]))
    SO2 = Decimal(str(reqBody["SO2"]))
    temp = Decimal(str(reqBody["temp"]))
    
    areaUID = reqBody["areaUID"]
    moduleID = reqBody["moduleID"]
    
    
    response = client.invoke_endpoint(
        EndpointName='pytorch-inference-2024-07-28-13-41-52-965', 
        ContentType='application/json',
        Body=json.dumps({"todays_aqi": int(str(AQI))})
    )
    response_body = response['Body']
    body_string = response_body.read().decode('utf-8')
    forecastedAQI = json.loads(body_string)['aqi_forcast']
    
    table.update_item(
            Key={
                'areaUID': areaUID
            },
            UpdateExpression=f'SET #a.#b.#c = :a, #a.#b.#d = :b, #a.#b.#e = :c, #a.#b.#f = :d, #a.#b.#g = :e, #a.#b.#h = :f, #a.#b.#i = :g, #a.#b.#j = :h, #a.#b.#k = :i, #a.#b.#l = :j, #a.#b.#m = :k, #a.#b.#n = :l',
            ExpressionAttributeValues={
                ':a': AQI,
                ':b': CO,
                ':c': humd,
                ':d': NH3,
                ':e': NO2,
                ':f': O3,
                ':g': PM10,
                ':h': PM25,
                ':i': SO2,
                ':j': temp,
                ':k': forecastedAQI,
                ':l': significant_pollutant,
            },
            ExpressionAttributeNames={
                '#a': 'aqi_modules',
                '#b': moduleID,
                '#c': 'AQI',
                '#d': 'CO',
                '#e': 'humd',
                '#f': 'NH3',
                '#g': 'NO2',
                '#h': 'O3',
                '#i': 'PM10',
                '#j': 'PM2.5',
                '#k': 'SO2',
                '#l': 'temp',
                '#m': 'aqi_forecast',
                '#n': 'significant_pollutant'
            },
            ReturnValues='ALL_NEW'
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('UPDATED')
    }
