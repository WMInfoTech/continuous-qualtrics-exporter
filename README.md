Symptom Tracker Data Processing Code  
====================================

This package contains scripts that will allow you to automate the export
of Qualtrics survey data and deliver it to OneDrive.

All the scripts contained in this project are simple, and can run standalone
if needed. This gives you the ability to fork and modify it in a way that is useful
to you. The overall project is a representation of how it can be used.

We understand that every use case may differ. This should get you past the
basics and move you right to the step where you process your survey results
and take action.

You can easily replace the OneDrive upload code with something else
to send the data to a reporting tool, another data storage service,
or read and act on the data in realtime. If you think your modification
might be useful to others, please consider opening a pull request.

At the bottom of this README you will find references to some sample code
that shows how to interact with the ModoLabs Communicate APIss that can be
used to send push notifications to your mobile app users based on data
pulled from your survey results.


## Requirements

This is built and tested using Python 3.8.3 and will run on Windows and Linux.

A requirements.txt file is included that lists all required pip packages. All of
this can be installed either globally, using python virtual environments, or run
in a container.

Additionally, we have an image available that can be used as is. The required
settings detailed below can be provided using any of the popular container
orchestration platforms. 

## Setup

This process requires several settings and a few secret values. There are three
general ways to manage all these inputs, and you can use a combination of the
three ways.

1. Set them all as environment variables. This is an acceptable approach for
   most values, but a few are considered secrets and should probably be managed
   differently. 
2. Set up a secrets directory and store values in files in that directory.
    * Set the environment variable `CV_SECRETS_PATH` equal to the directory name.
    * Create a file for each value where the file name should be the required setting. For example, your file name would be `QUALTRICS_CLIENTID` and the file would contain a single entry with the value of the clientid. This approach will also work for any or all required settings. 
    * Build a config.yml file that contains any or all settings. You will need the environment variable `CV_CONFIG_PATH` set equal to the directory where you will store this file. 
    * The file format should be 
```yaml
    settings:  
        QUALTRICS_DATACENTER: xxxxx.cal
        QUALTRICS_SURVEYID: YOURSURVEYID123
```
### Required Settings

* `QUALTRICS_DATACENTER`
    * The Qualtrics datacenter for your instance of Qualtrics  
* `QUALTRICS_SURVEYID`
    * The survey id for which you intend to export data
* `QUALTRICS_CLIENTID`
    * The Qualtrics API client id configured through Qualtrics
* `QUALTRICS_UPLOADPATH`
    * If writing the export file locally, you need to define the path to the location you want to save the file
* `QUALTRICS_UPLOADFILE`
    * The name you want to give the export file. For example, "responses" You do not need to add ".zip" it will do that as part of the download. 
* `MS_AUTHORITY`
    * Required for conecting to the MSGraph API...generally the value should be https://login.microsoftonline.com
* `MS_TENANT`
    * The ID for your O365 tenant
* `MS_RESOURCE`
    * https://graph.microsoft.com
* `MS_CLIENTID`
    * Your api clientid
* `MS_CLIENTCERT`
    * The path to your clientcert required for the MSGraph API...for example "/opt/mscert/mycert.pem"
* `MS_USER`
    * The MS OneDrive user account you are uploading to. theuser@yourdomain.edu
* `MS_USERFOLDER`
    * The folder that is one level up from your root OneDrive folder...for example "SurveyExports"
* `CV_SECRETS_PATH`
    * This is the path to your secrets directory. This is only available to be set as an environment variable
* `CV_CONFIG_PATH`
    * This is the path to your optional config.yml file. This is only available to be set as an environment variable. This can be used to define all the settings described in this list except `CV_CONFIG_PATH` and `CV_SECRETS_PATH`
* `LOOP_DELAY`
    * If running this as a service, how long in seconds between exports. 
* `TIME_BUFFER`
    * How far back from the current time should the data be exported in hours. 
* `QUALTRICS_EXPORTFORMAT`
    * Available options are `json` or `csv`
* `MS_UNIQEFILENAME`
    * If running this as a continuous service, you can set this flag to "True" and it will generate unique filenames for the export files so you can run it frequently without overwriting existing files. 

### Included Scripts

- gettoken.py
    * Connects to Qualtrics to get required Bearer token for authentication
    * To generate the clientid and secret, follow the Qualtrics documentation API OAuth Section [available here](https://www.qualtrics.com/support/integrations/api-integration/overview/)
    * To find your Qualtrics datacenter ID, [read here](https://www.qualtrics.com/support/integrations/api-integration/finding-qualtrics-ids/)
    * Required inputs:
        * `QUALTRICS_CLIENTID`
        * `QUALTRICS_SECRET`
        * `QUALTRICS_DATACENTER`
    * Returns `bearerToken` used for subsequent Qualtrics API calls
    * Direct usage example
        * `python gettoken.py`
- generateexport.py
    * Connects to the Qualtrics API using the Bearertoken generated from gettoken.py and starts the export process.
    * Required inputs:
        * `QUALTRICS_DATACENTER`
        * `QUALTRICS_SURVEYID`
        * `bearerToken`
        * `QUALTRICS_EXPORTFORMAT` - Can be either `csv` or `json`
    * Returns `progress_id` used in exportprogress.py script
    * Direct usage example
        * `python generateexport.py --bearerToken [bearerToken]`
- exportprogress.py
    * Checks the export progress and continues checking until it responds as complete
    * Required inputs
        * `QUALTRICS_DATACENTER`
        * `QUALTRICS_SURVEYID`
        * `progress_id`
        * `bearerToken`
    * Returns `file_id` used in exportfiledownload.py
    * Direct usage example
        * `exportprogress.py --progressId [progress_id] --bearerToken [bearerToken]`
- exportfiledownload.py
    * Downloads zip file from Qualtrics in containing export file in format specified during generateexport.py
    * Required inputs
        * `QUALTRICS_DATACENTER`
        * `QUALTRICS_SURVEYID`
        * `file_id`
        * `bearerToken`
    * Optional additional inputs
        * `downloadfile` = None - Path and filename for writing the file. Defaults to None and is only required if you intend to download and write the file locally
        * `wrtiefile` = False - True or False and tells the process to write the file locally. Defaults to False and is only required if you intend to download and write the file locally
    * Returns None if writing file locally. If this is used to hand off a file object to another process such as uploading to OneDrive, Box, or GoogleDrive, it will return a fileobject without writing it locally. 
    * Direct usage example
        * `exportfiledownload.py --fileId [file_id] --bearerToken [bearerToken]`
- uploadtoonedrive.py
    * Uploads file object returned from exportfiledownload.py to OneDrive folder
    * Required inputs
        * `MS_AUTHORITY`
        * `MS_TENANT`
        * `MS_RESOURCE`
        * `MS_CLIENTID`
        * `MS_THUMBPRINT`
        * `MS_CLIENTCERT`
        * `MS_USER`
        * `MS_USERFOLDER`
        * `MS_UNIQEFILENAME`
        * `fileobject` = None - Output of exportdownloadfile.py if the direct stream to OneDrive options is used. Otherwise, set to None
        * `QUALTRICS_UPLOADFILE` - Desired filename when written to OneDrive
        * `uploadfilepath` = None - If file was downloaded locally before being uploaded to OneDrive, the path to the file
    * Returns a Success or Failed message
    * Direct usage example (will only work directly if file is written locally)
        * `uploadtoonedrive.py`

## Contributions

We welcome contributions to this project. Feel free to open an issue or pull request.

## Modo Labs API Information

Also included in this code are two scripts that can be used to manage push notifications
through the ModoLabs mobile platform. This functionality requires the Communicate Premium
feature. I recommend reading Modo support documentation on how to generate the two required
tokens needed to use these APIs, setting up the directory and the personal channel and
documentation on the appropriate file scructure of the notification directory. 

* modonewdirectory.py
    * Takes a local directory xml file and will upload it to Modo and enable it as the current directory. 
* modopersonalmessage.py
    * Pushes a notification to the personal channel defined by the token used for authenticating to the API. 
