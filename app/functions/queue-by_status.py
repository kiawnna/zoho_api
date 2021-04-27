from app import zoho_auth_function
import os
import boto3
import json
from datetime import datetime
BUCKET = os.environ['BUCKET']


def main(event, context):
    s3 = boto3.client('s3')
    status = event['status']
    params = f'?status={status}'
    base_path = 'ticketsByStatus'
    path = f'{base_path}{params}'

    try:
        now = datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
        result = zoho_auth_function.main(path)
        response = result['body']['data']

        s3.put_object(
            Body=str(json.dumps(response)),
            Bucket=BUCKET,
            Key=f'queue/{base_path}/{status}/{now}.json'
        )
    except Exception as e:
        return str(e)

