__author__ = 'jwpully'
import requests
import json

def getsurveyid(dataCenter, bearerToken, surveyname):
    try:
        baseUrl = "https://{0}.qualtrics.com/API/v3/surveys".format(dataCenter)
        headers = {
            "authorization": "bearer " + bearerToken,
            }

        response = requests.request("GET", baseUrl, headers=headers)
        for item in json.loads(response.text)['result']['elements']:
            if item['name'] == surveyname:
                survey_id = item['id']

        return survey_id
    except Exception as e:
        print("An error occurred while getting the Qualtrics survey ID")
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

    if 'QUALTRICS_DATACENTER' in secrets:
        QUALTRICS_DATACENTER = secrets['QUALTRICS_DATACENTER']
    else:
        QUALTRICS_DATACENTER = os.getenv("QUALTRICS_DATACENTER", None)

    if 'QUALTRICS_BEARERTOKEN' in secrets:
        QUALTRICS_BEARERTOKEN = secrets['QUALTRICS_BEARERTOKEN']
    else:
        QUALTRICS_BEARERTOKEN = os.getenv("QUALTRICS_BEARERTOKEN", None)

    if 'QUALTRICS_SURVEYNAME' in secrets:
        QUALTRICS_SURVEYNAME = secrets['QUALTRICS_SURVEYNAME']
    else:
        QUALTRICS_SURVEYNAME = os.getenv("QUALTRICS_SURVEYNAME", None)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataCenter", help="Qualtrics Data Center", default=QUALTRICS_DATACENTER)
    parser.add_argument("-t", "--bearerToken", help="Token generated from gettoken", default=QUALTRICS_BEARERTOKEN)
    parser.add_argument("-s", "--surveyname", help="The Survey name you are looking up", default=QUALTRICS_SURVEYNAME)
    args = parser.parse_args()
    print(getsurveyid(args.dataCenter, args.bearerToken, args.surveyname))