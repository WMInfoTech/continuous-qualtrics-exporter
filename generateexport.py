__author__ = 'jwpully'
import requests
import json

def generateexport(dataCenter, survey_id, bearerToken, startDate=None, endDate=None):
    # Attempt to export responses

    try:
        baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses".format(dataCenter, survey_id)
        print(baseUrl)

        headers = {
            "authorization": "bearer " + bearerToken,
             "Content-Type": "application/json"
            }

        json_string = {"format": "json"}

        if startDate is not None:
            json_string['startDate'] = startDate

        if endDate is not None:
            json_string['endDate'] = endDate

        response = requests.request("POST", baseUrl, json=json_string, headers=headers)
        print(response.text)
        return json.loads(response.text)['result']['progressId']

    except Exception as e:
        print("An error occurred while generating the Qualtrics survey export")
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

    if 'QUALTRICS_SURVEYID' in secrets:
        QUALTRICS_SURVEYID = secrets['QUALTRICS_SURVEYID']
    else:
        QUALTRICS_SURVEYID = os.getenv("QUALTRICS_SURVEYID", None)

    if 'QUALTRICS_BEARERTOKEN' in secrets:
        QUALTRICS_BEARERTOKEN = secrets['QUALTRICS_BEARERTOKEN']
    else:
        QUALTRICS_BEARERTOKEN = os.getenv("QUALTRICS_BEARERTOKEN", None)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataCenter", help="Qualtrics Data Center", default=QUALTRICS_DATACENTER)
    parser.add_argument("-s", "--survey_id", help="The Survey id from getsurveyid", default=QUALTRICS_SURVEYID)
    parser.add_argument("-t", "--bearerToken", help="Token generated from gettoken", default=QUALTRICS_BEARERTOKEN)
    parser.add_argument("-b", "--startDate", help="Start Date of recorded range", default=None)
    parser.add_argument("-e", "--endDate", help="End date of recorded range", default=None)
    args = parser.parse_args()
    print(generateexport(args.dataCenter, args.survey_id, args.bearerToken, args.startDate, args.endDate))