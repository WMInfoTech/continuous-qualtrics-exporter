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
    from app.configmanager import settings

    try:
        settings = settings()
        bearerToken = gettoken(settings['QUALTRICS_CLIENTID'], settings['QUALTRICS_SECRET'], settings['QUALTRICS_DATACENTER'])
        print("Next command, execute:")
        print("python generateexport.py --bearerToken " + bearerToken)
    except Exception as e:
        print("An error occurred while running gettoken")
        print(str(e))