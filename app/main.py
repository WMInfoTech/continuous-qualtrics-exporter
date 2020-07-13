import os
import signal
import time
from datetime import datetime, timedelta
from lib.configmanager import settings
from lib.exportfiledownload import exportfiledownload
from lib.exportprogress import exportprogress
from lib.generateexport import generateexport
from lib.gettoken import gettoken
from lib.uploadtoonedrive import uploadtoonedrive

settings = settings()

def receiveSignal(signalNumber, frame):
    print("Received: ", signalNumber)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, receiveSignal)
    signal.signal(signal.SIGTERM, receiveSignal)

    while True:

        print("Attempting to retreive Qualtrics Bearer token")
        bearerToken = gettoken(settings['QUALTRICS_CLIENTID'], settings['QUALTRICS_SECRET'], settings['QUALTRICS_DATACENTER'])
        print("Retreived Qualtrics Bearer token")

        dt1 = datetime.now()
        dt2 = dt1 - timedelta(hours=int(settings['TIME_BUFFER']))

        dt1 = dt1.strftime("%Y-%m-%dT%H:%M:%SZ")
        dt2 = dt2.strftime("%Y-%m-%dT%H:%M:%SZ")
        print("Generating export from {0} to {1}".format(dt2, dt1))

        # survey_id = getsurveyid(dataCenter, bearerToken, 'COVID19 - Screener - TEST')
        print("Starting Qualtrics export")
        progress_id = generateexport(settings['QUALTRICS_DATACENTER'], settings['QUALTRICS_SURVEYID'], bearerToken, settings['QUALTRICS_EXPORTFORMAT'], dt2, dt1)
        print("Started Qualtrics export")

        print("Tracking Qualtrics export progress")
        file_id = exportprogress(settings['QUALTRICS_DATACENTER'], settings['QUALTRICS_SURVEYID'], progress_id, bearerToken)
        print("Qualtrics export complete and Download File ID retreived")

        print("Downloading Qualtrics Export File")
        fileobject = exportfiledownload(settings['QUALTRICS_DATACENTER'], settings['QUALTRICS_SURVEYID'], file_id, bearerToken)
        print("Downloaded Qualtrics Export File")

        # unzipfile()
        #
        # readfile()

        print("Uploading Qualtrics File to OneDrive")
        uploadtoonedrive(settings['MS_AUTHORITY']
        , settings['MS_TENANT'], settings['MS_RESOURCE'], settings['MS_CLIENTID']
        , settings['MS_THUMBPRINT'], settings['MS_CLIENTCERT'], settings['MS_USER'], settings['MS_USERFOLDER'], settings['MS_UNIQEFILENAME'], fileobject, settings['QUALTRICS_UPLOADFILE'])
        print("Uploaded Qualtrics File to OneDrive")

        print("Sleeping for {0} seconds".format(str(settings['LOOP_DELAY'])))
        time.sleep(int(settings['LOOP_DELAY']))