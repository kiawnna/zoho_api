from app import zoho_auth_function
import os
import boto3
import json
from datetime import datetime
BUCKET = os.environ['BUCKET']


def main(event, context):
    s3 = boto3.client('s3')
    ticket_id = '511401000000141411'
    path = f'tickets/{ticket_id}/threads'
    try:
        now = datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
        result = zoho_auth_function.main(path)
        response = result['body']['data']['author']

        s3.put_object(
            Body=str(json.dumps(response)),
            Bucket=BUCKET,
            Key=f'threads/ticketId:{ticket_id}/{now}.json'
        )
    except Exception as e:
        return str(e)
