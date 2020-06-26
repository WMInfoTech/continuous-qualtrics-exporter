__author__ = 'jwpully'
import requests

def modonewdirectory(token):
    try:
        baseUrl = "https://communicate.modolabs.net/api/v1/directories/revisions/"

        headers = {
            "Authorization": "Token " + token,
            }

        files = {'upload': ('allwm.xml', open('data/allwm.xml', 'rb'), 'application/xml', {'Expires': '0'})}
        values = {'name': 'allWM_V2_w3users'}
        response = requests.request("POST", baseUrl, files=files, data=values, headers=headers)

        for item in response:
            print(item)
    except Exception as e:
        print("There was an error uploading a new directory to modo")
        print(str(e))
        exit(1)

if __name__ == "__main__":
    import argparse
    import os
    from secretsmanager import secretsmanager

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
    print(modonewdirectory(args.token))