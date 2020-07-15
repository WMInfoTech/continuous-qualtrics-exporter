Symptom Tracker Data Processing Code  
====================================

Current Features:  
- Export results from Qualtrics by date/time range
- Upload export to OneDrive
- Update ModoLabs Directory
- Submit message to personal channel through ModoLabs API

ToDo:
- Develop way to track export date/time ranges
- Analyze respondents and compare to dataset of expected respondents
- Build ModoLabs directory for upload
- Verify recently uploaded ModoLabs directory is currently active
- Build export from Microsoft Forms
- Develop notification process based on responses

Description:
- gettoken.py
    * Connects to Qualtrics to get required Bearer token for authentication
    * To generate the clientid and secret, follow the Qualtrics documentation API OAuth Section [available here](https://www.qualtrics.com/support/integrations/api-integration/overview/)
    * To find your Qualtrics datacenter ID, [read here](https://www.qualtrics.com/support/integrations/api-integration/finding-qualtrics-ids/)
    * Required inputs:
        * QUALTRICS_CLIENTID
        * QUALTRICS_SECRET
        * QUALTRICS_DATACENTER
    * Returns `bearerToken` used for subsequent Qualtrics API calls
    * Direct usage example
        * `python gettoken.py`
- generateexport.py
    * Connects to the Qualtrics API using the Bearertoken generated from gettoken.py and starts the export process.
    * Required inputs:
        * QUALTRICS_DATACENTER
        * QUALTRICS_SURVEYID
        * `bearerToken`
        * QUALTRICS_EXPORTFORMAT - Can be either `csv` or `json`
    * Returns `progress_id` used in exportprogress.py script
    * Direct usage example
        * `python generateexport.py --bearerToken [bearerToken]`
- exportprogress.py
    * Checks the export progress and continues checking until it responds as complete
    * Required inputs
        * QUALTRICS_DATACENTER
        * QUALTRICS_SURVEYID
        * `progress_id`
        * `bearerToken`
    * Returns `file_id` used in exportfiledownload.py
    * Direct usage example
        * `exportprogress.py --progressId [progress_id] --bearerToken [bearerToken]`
- exportfiledownload.py
    * Downloads zip file from Qualtrics in containing export file in format specified during generateexport.py
    * Required inputs
        * QUALTRICS_DATACENTER
        * QUALTRICS_SURVEYID
        * `file_id`
        * `bearerToken`
    * Optional additional inputs
        * `downloadfile` = None - Path and filename for writing the file.  Defaults to None and is only required if you intend to download and write the file locally
        * `wrtiefile` = False - True or False and tells the process to write the file locally.  Defaults to False and is only required if you intend to download and write the file locally
    * Returns None if writing file locally.  If this is used to hand off a file object to another process such as uploading to OneDrive, Box, or GoogleDrive, it will return a fileobject without writing it locally.  
    * Direct usage example
        * `exportfiledownload.py --fileId [file_id] --bearerToken [bearerToken]`
- uploadtoonedrive.py
    * Uploads file object returned from exportfiledownload.py to OneDrive folder
    * Required inputs
        * MS_AUTHORITY
        * MS_TENANT
        * MS_RESOURCE
        * MS_CLIENTID
        * MS_THUMBPRINT
        * MS_CLIENTCERT
        * MS_USER
        * MS_USERFOLDER
        * MS_UNIQEFILENAME
        * `fileobject` = None - Output of exportdownloadfile.py if the direct stream to OneDrive options is used.  Otherwise, set to None
        * QUALTRICS_UPLOADFILE - Desired filename when written to OneDrive
        * `uploadfilepath` = None - If file was downloaded locally before being uploaded to OneDrive, the path to the file
    * Returns a Success or Failed message
    * Direct usage example (will only work directly if file is written locally)
        * `uploadtoonedrive.py`








































