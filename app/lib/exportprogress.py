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
            response = requests.request("GET", baseUrl, headers=headers)

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
    from configmanager import settings

    try:
        settings = settings()

        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--progressId", help="The progress id from generateexport", default=None)
        parser.add_argument("-t", "--bearerToken", help="Token generated from gettoken", default=None)
        args = parser.parse_args()

        if args.progressId is None or args.bearerToken is None:
            print("A Bearer token and progressId are required on the command line")
            print("python exportprogress.py --bearerToken XXXXXXXXXX --progressId YYYYYYYYYYY")
            print("The bearerToken can be generated by running gettoken.py")
            print("The progressId can be generated by running generateexport.py")
        else:
            fileId = exportprogress(settings['QUALTRICS_DATACENTER'], settings['QUALTRICS_SURVEYID'], args.progressId, args.bearerToken)
            print("Next command, execute:")
            print("python exportfiledownload.py --bearerToken " + args.bearerToken + " --fileId " + fileId)
    except Exception as e:
        print("An error occurred while checking the export progress")
        print(str(e))