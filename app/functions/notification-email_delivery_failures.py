from app import zoho_auth_function
import os
import boto3
import json
from datetime import datetime
BUCKET = os.environ['BUCKET']


def main(event, context):
    s3 = boto3.client('s3')
    department_id = event['department_id']
    params = f'?department={department_id}'
    base_path = 'emailFailureAlerts'
    path = f'{base_path}{params}'
    try:
        now = datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
        result = zoho_auth_function.main(path)
        response = result['body']['data']

        s3.put_object(
            Body=str(json.dumps(response)),
            Bucket=BUCKET,
            Key=f'notifications/{base_path}/departmentId:{department_id}/{now}.json'
        )
    except Exception as e:
        return str(e)
