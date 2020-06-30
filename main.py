import os
from app.configmanager import settings
from app.exportfiledownload import exportfiledownload
from app.exportprogress import exportprogress
from app.generateexport import generateexport
from app.gettoken import gettoken
from app.uploadtoonedrive import uploadtoonedrive

settings = settings()

# exit()
#
# if os.getenv("DATETIMEMANAGER", "sqlite") == "sqlite":
#     from app.datetime_manager import DateTimeManager_SQLite
#     datetimemanager = DateTimeManager_SQLite()
#
# datetimemanager.connect()
# start_time = datetimemanager.select_datetime()
# end_time = datetimemanager.selection_window()
#
# print(start_time)
# print(end_time)
#
# exit()

bearerToken = gettoken(settings['QUALTRICS_CLIENTID'], settings['QUALTRICS_SECRET'], settings['QUALTRICS_DATACENTER'])

# survey_id = getsurveyid(dataCenter, bearerToken, 'COVID19 - Screener - TEST')

progress_id = generateexport(settings['QUALTRICS_DATACENTER'], settings['QUALTRICS_SURVEYID'], bearerToken, "2020-06-11T00:00:00Z", "2020-06-11T23:59:59Z")

file_id = exportprogress(settings['QUALTRICS_DATACENTER'], settings['QUALTRICS_SURVEYID'], progress_id, bearerToken)

exportfiledownload(settings['QUALTRICS_DATACENTER'], settings['QUALTRICS_SURVEYID'], file_id, bearerToken, os.path.join(settings['QUALTRICS_UPLOADPATH'], settings['QUALTRICS_UPLOADFILE']))

# unzipfile()
#
# readfile()

uploadtoonedrive(settings['QUALTRICS_UPLOADPATH'], settings['QUALTRICS_UPLOADFILE'], settings['MICROSOFT_AUTHORITY']
, settings['MICROSOFT_TENANT'], settings['MICROSOFT_RESOURCE'], settings['MICROSOFT_CLIENTID']
, settings['MICROSOFT_THUMBPRINT'], settings['MICROSOFT_CERT'], settings['MICROSOFT_USER'], settings['MICROSOFT_USERFOLDER'])