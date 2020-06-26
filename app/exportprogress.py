__author__ = 'jwpully'
import requests
import json
import time

def exportprogress(dataCenter, survey_id, progress_id, bearerToken):
    # Export progress
    try:
        export_status = None

        while export_status != "complete":

            baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/{2}".format(dataCenter, survey_id, progress_id)
            print(baseUrl)

            headers = {
                "authorization": "bearer " + bearerToken,
                 "Content-Type": "application/json"
                }
            # json = {"format": "json"}

            response = requests.request("GET", baseUrl, headers=headers)
            print(response.text)

            if json.loads(response.text)['result']['status'] == 'complete':
                print("Export is complete, moving on to download")
                export_status = json.loads(response.text)['result']['status']
                file_id = json.loads(response.text)['result']['fileId']
                return file_id
            else:
                print("Export is not complete")
                print("Waiting 10 seconds then trying again")
                time.sleep(10)
    except Exception as e:
        print("An error occurred while monitoring export progress")
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

    if 'QUALTRICS_DATACENTER' in secrets:
        QUALTRICS_DATACENTER = secrets['QUALTRICS_DATACENTER']
    else:
        QUALTRICS_DATACENTER = os.getenv("QUALTRICS_DATACENTER", None)

    if 'QUALTRICS_SURVEYID' in secrets:
        QUALTRICS_SURVEYID = secrets['QUALTRICS_SURVEYID']
    else:
        QUALTRICS_SURVEYID = os.getenv("QUALTRICS_SURVEYID", None)

    if 'QUALTRICS_PROGRESSID' in secrets:
        QUALTRICS_PROGRESSID = secrets['QUALTRICS_PROGRESSID']
    else:
        QUALTRICS_PROGRESSID = os.getenv("QUALTRICS_PROGRESSID", None)

    if 'QUALTRICS_BEARERTOKEN' in secrets:
        QUALTRICS_BEARERTOKEN = secrets['QUALTRICS_BEARERTOKEN']
    else:
        QUALTRICS_BEARERTOKEN = os.getenv("QUALTRICS_BEARERTOKEN", None)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataCenter", help="Qualtrics Data Center", default=QUALTRICS_DATACENTER)
    parser.add_argument("-s", "--survey_id", help="The Survey id from getsurveyid", default=QUALTRICS_SURVEYID)
    parser.add_argument("-p", "--progress_id", help="The progress id from generateexport", default=QUALTRICS_PROGRESSID)
    parser.add_argument("-t", "--bearerToken", help="Token generated from gettoken", default=QUALTRICS_BEARERTOKEN)
    args = parser.parse_args()
    print(exportprogress(args.dataCenter, args.survey_id, args.progress_id, args.bearerToken))