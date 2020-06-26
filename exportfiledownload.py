__author__ = 'jwpully'
import requests

def exportfiledownload(dataCenter, survey_id, file_id, bearerToken):
    # Export file download
    try:
        baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/{2}/file".format(dataCenter, survey_id, file_id)
        print(baseUrl)

        headers = {
            "authorization": "bearer " + bearerToken,
             "Content-Type": "application/json"
            }

        response = requests.request("GET", baseUrl, headers=headers)

        with open('data/responses.zip', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        print(response.status_code)
    except Exception as e:
        print("An error occurred while downloading your export file")
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

    if 'QUALTRICS_FILEID' in secrets:
        QUALTRICS_FILEID = secrets['QUALTRICS_FILEID']
    else:
        QUALTRICS_FILEID = os.getenv("QUALTRICS_FILEID", None)

    if 'QUALTRICS_BEARERTOKEN' in secrets:
        QUALTRICS_BEARERTOKEN = secrets['QUALTRICS_BEARERTOKEN']
    else:
        QUALTRICS_BEARERTOKEN = os.getenv("QUALTRICS_BEARERTOKEN", None)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataCenter", help="Qualtrics Data Center", default=QUALTRICS_DATACENTER)
    parser.add_argument("-s", "--survey_id", help="The Survey id from getsurveyid", default=QUALTRICS_SURVEYID)
    parser.add_argument("-p", "--file_id", help="The progress id from exportprogress", default=QUALTRICS_FILEID)
    parser.add_argument("-t", "--bearerToken", help="Token generated from gettoken", default=QUALTRICS_BEARERTOKEN)
    args = parser.parse_args()
    exportfiledownload(args.dataCenter, args.survey_id, args.file_id, args.bearerToken)