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
    * Required inputs:
        * QUALTRICS_CLIENTID
        * QUALTRICS_SECRET
        * QUALTRICS_DATACENTER
- generateexport.py
    * Connects to the Qualtrics API using the Bearertoken generated from gettoken.py and starts the export process.
    * Required inputs:
        * QUALTRICS_DATACENTER
        * QUALTRICS_SURVEYID
        * QUALTRICS_BEARERTOKEN
