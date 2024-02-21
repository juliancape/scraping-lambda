import json
import boto3
from datetime import datetime
import urllib.request

def lambda_handler(event, context):
    current_datetime = datetime.utcnow()

    if current_datetime.hour == 20 and current_datetime.minute == 30:
        eltiempo_url = 'https://www.eltiempo.com/'

        with urllib.request.urlopen(eltiempo_url) as response:
            page_content = response.read().decode('utf-8')

        if response.code == 200:
            filename = f'{current_datetime.strftime('%Y-%m-%d')}.html'

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
    else:
        print('Sin ejecutar')
        return {
            'statusCode': 200,
            'body': json.dumps('La función no se ejecutó en este momento.')
        }
