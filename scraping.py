import json
import boto3
from datetime import datetime
import urllib.request

def lambda_handler(event, context):
    current_datetime = datetime.now().strftime('%Y-%m-%d')

    eltiempo_url = 'https://www.eltiempo.com/'
    ruq = urllib.request.Request(eltiempo_url, headers={'User-agent': 'Mozilla/5.0'})    
    with urllib.request.urlopen(ruq) as response:
        page_content = response.read().decode('utf-8')

    if response.code == 200:
        filename = f'{current_datetime}.html'

        s3 = boto3.client('s3', region_name='us-east-1')

        s3.put_object(Body=page_content, Bucket='eltiempo-julian', Key=filename)
        print('Ejecutado')
        return {
            'statusCode': 200,
            'body': json.dumps(f'Se ha descargado y guardado la página del tiempo en {filename}')
        }
    else:
        print('Error')
        return {
            'statusCode': response.code,
            'body': json.dumps(f'Error al descargar la página del tiempo. Código de estado: {response.code}')
        }
