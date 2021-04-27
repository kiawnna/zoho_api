import requests
import json
import boto3
import os


def main(path):
    secret_id = os.environ['SECRET_ID']
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(
            SecretId=secret_id
        )
        secret = eval(response['SecretString'])

        if 'access_token' in secret:
            refresh_token = secret['refresh_token']
            try:
                headers = {'orgId': secret['org_id'], 'Authorization': f'Zoho-oauthtoken {secret["access_token"]}'}
                payload = requests.get(f'https://desk.zoho.com/api/v1/{path}', headers=headers).json()

                if 'errorCode' in payload:
                    refresh_access_token_params = {
                        "client_id": secret['client_id'],
                        "client_secret": secret['client_secret'],
                        "refresh_token": refresh_token,
                        "grant_type": "refresh_token",
                        "redirect_uri": secret['redirect_uri'],
                        "scope": "Desk.tickets.ALL,Desk.tasks.ALL,Desk.settings.ALL,Desk.search.READ,Desk.events.ALL,"
                                 "Desk.articles.READ,Desk.articles.CREATE,Desk.articles.UPDATE,Desk.articles.DELETE,"
                                 "Desk.contacts.READ,Desk.contacts.WRITE,Desk.contacts.UPDATE,Desk.contacts.CREATE,"
                                 "Desk.basic.READ,Desk.basic.CREATE,AAAServer.profile.ALL"
                    }
                    refresh_access_token = requests.post('https://accounts.zoho.com/oauth/v2/token',
                                                         params=refresh_access_token_params)
                    refresh_access_token_content = json.loads(refresh_access_token.text)
                    secret['access_token'] = refresh_access_token_content['access_token']
                    client.put_secret_value(
                        SecretId=secret_id,
                        SecretString=f'{secret}'
                    )
                    headers = {'orgId': secret['org_id'], 'Authorization': f'Zoho-oauthtoken {secret["access_token"]}'}
                    payload = requests.get(f'https://desk.zoho.com/api/v1/{path}', headers=headers).json()

                    return {
                        'statusCode': 200,
                        'body': payload
                    }

                else:

                    return {
                        'statusCode': 200,
                        'body': payload
                    }

            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        "error": str(e)
                    })
                }
        else:
            access_token_params = {
                "code": secret['code'],
                "client_id": secret['client_id'],
                "client_secret": secret['client_secret'],
                "grant_type": "authorization_code",
                "redirect_uri": secret['redirect_uri'],
                "access_type": "offline",
                "prompt": "consent"
            }
            get_access_token = requests.post('https://accounts.zoho.com/oauth/v2/token',
                                             params=access_token_params).json()
            secret['access_token'] = get_access_token['access_token']
            secret['refresh_token'] = get_access_token['refresh_token']
            client.put_secret_value(
                SecretId=secret_id,
                SecretString=f'{secret}'
            )
            try:
                headers = {'orgId': secret['org_id'], 'Authorization': f'Zoho-oauthtoken {secret["access_token"]}'}
                payload = requests.get(f'https://desk.zoho.com/api/v1/{path}', headers=headers).json()

                return {
                    'statusCode': 200,
                    'body': json.dumps(payload)
                }
            except Exception as e:
                return {
                    'statusCode': 501,
                    'body': str(e)
                }
    except Exception as e:
        return {
            'statusCode': 501,
            'body': str(e)
        }
