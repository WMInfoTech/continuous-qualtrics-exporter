__author__ = 'jwpully'
import requests

def modopersonalmessage(token):
    try:
        baseUrl = "https://communicate.modolabs.net/api/v1/messages/personal/"

        headers = {
            "Authorization": "Token " + token,
            "Content-Type": "application/json"
            }




        values = {'title': 'Test Sending a link by API'
                  , 'body': 'Testing a link....can I click this https://www.wm.edu'
                  , 'style': 'information'
                  , 'send_tag': 'university'
                  , 'push_notifications': True}
        response = requests.request("POST", baseUrl, json=values, headers=headers)

        for item in response:
            print(item)
    except Exception as e:
        print("There was an error pushing a new personal message")
        print(str(e))
        exit(1)

if __name__ == "__main__":
    import argparse
    import os
    from app.secretsmanager import secretsmanager

    secrets_path = os.getenv("CV_SECRETS_PATH", None)
    if secrets_path is not None:
        secrets = secretsmanager(secrets_path)
    else:
        secrets = {}

    if 'MODO_TOKEN' in secrets:
        MODO_TOKEN = secrets['MODO_TOKEN']
    else:
        MODO_TOKEN = os.getenv("MODO_TOKEN", None)

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", help="Token from Modo org level directory configuration", default=MODO_TOKEN)
    args = parser.parse_args()
    print(modopersonalmessage(args.token))