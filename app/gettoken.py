__author__ = 'jwpully'
import requests

def gettoken(clientId, clientSecret, dataCenter):

    try:
        baseUrl = "https://{0}.qualtrics.com/oauth2/token".format(dataCenter)
        data = { "grant_type": "client_credentials" }

        r = requests.post(baseUrl, auth=(clientId, clientSecret), data=data)

        return r.json()['access_token']
    except Exception as e:
        print("An error occurred while getting the Qualtrics Token")
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

    if 'QUALTRICS_CLIENTID' in secrets:
        QUALTRICS_CLIENTID = secrets['QUALTRICS_CLIENTID']
    else:
        QUALTRICS_CLIENTID = os.getenv("QUALTRICS_CLIENTID", None)

    if 'QUALTRICS_SECRET' in secrets:
        QUALTRICS_SECRET = secrets['QUALTRICS_SECRET']
    else:
        QUALTRICS_SECRET = os.getenv("QUALTRICS_SECRET", None)

    if 'QUALTRICS_DATACENTER' in secrets:
        QUALTRICS_DATACENTER = secrets['QUALTRICS_DATACENTER']
    else:
        QUALTRICS_DATACENTER = os.getenv("QUALTRICS_DATACENTER", None)

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--clientId", help="Qualtrics Client ID", default=QUALTRICS_CLIENTID)
    parser.add_argument("-s", "--clientSecret", help="Qualtrics Secret", default=QUALTRICS_SECRET)
    parser.add_argument("-d", "--dataCenter", help="Qualtrics Data Center", default=QUALTRICS_DATACENTER)
    args = parser.parse_args()
    print(gettoken(args.clientId, args.clientSecret, args.dataCenter))