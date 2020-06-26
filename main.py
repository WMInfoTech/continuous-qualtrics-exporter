import os
from secretsmanager import secretsmanager

from readfile import readfile
from unzipfile import unzipfile
from exportfiledownload import exportfiledownload
from exportprogress import exportprogress
from generateexport import generateexport
from getsurveyid import getsurveyid
from gettoken import gettoken
from uploadtoonedrive import uploadtoonedrive

secrets_path = os.getenv("CV_SECRETS_PATH", None)
if secrets_path is not None:
    secrets = secretsmanager(secrets_path)
else:
    secrets = {}



bearerToken = gettoken(secrets['QUALTRICS_CLIENTID'], secrets['QUALTRICS_SECRET'], secrets['QUALTRICS_DATACENTER'])

# survey_id = getsurveyid(dataCenter, bearerToken, 'COVID19 - Screener - TEST')

progress_id = generateexport(secrets['QUALTRICS_DATACENTER'], secrets['QUALTRICS_SURVEYID'], bearerToken, "2020-06-11T00:00:00Z", "2020-06-11T23:59:59Z")

file_id = exportprogress(secrets['QUALTRICS_DATACENTER'], secrets['QUALTRICS_SURVEYID'], progress_id, bearerToken)

exportfiledownload(secrets['QUALTRICS_DATACENTER'], secrets['QUALTRICS_SURVEYID'], file_id, bearerToken)

# unzipfile()
#
# readfile()

uploadtoonedrive(secrets['MICROSOFT_ULPATH'], secrets['MICROSOFT_ULFILENAME'], secrets['MICROSOFT_AUTHORITY']
, secrets['MICROSOFT_TENANT'], secrets['MICROSOFT_RESOURCE'], secrets['MICROSOFT_CLIENTID']
, secrets['MICROSOFT_THUMBPRINT'], secrets['MICROSOFT_CERT'], secrets['MICROSOFT_USER'], secrets['MICROSOFT_USERFOLDER'])