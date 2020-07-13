import yaml
import os

def envvarmanager():
    envvars = ('QUALTRICS_CLIENTID'
    , 'QUALTRICS_CLIENTSECRET'
    , 'QUALTRICS_DATACENTER'
    , 'QUALTRICS_SURVEYID'
    , 'QUALTRICS_STARTDATE'
    , 'QUALTRICS_TIMEWINDOW'
    , 'QUALTRICS_UPLOADPATH'
    , 'QUALTRICS_UPLOADFILE'
    , 'MS_AUTHORITY'
    , 'MS_TENANT'
    , 'MS_RESOURCE'
    , 'MS_CLIENTID'
    , 'MS_THUMBPRINT'
    , 'MS_CLIENTCERT'
    , 'MS_USER'
    , 'MS_USERFOLDER'
    , 'MODO_DIRECTORYTOKEN'
    , 'MODO_CHANNELTOKEN'
    , 'SQLITE_DBPATH'
    , 'DATETIMEMANAGER'
    , 'SURVEY_TIMEWINDOW'
    , 'LOOP_DELAY'
    , 'TIME_BUFFER'
    , 'QUALTRICS_EXPORTFORMAT'
    , 'MS_UNIQEFILENAME')

    envvar_values = {}
    for envvar in envvars:
        if os.getenv(envvar) is not None:
            envvar_values[envvar] = os.getenv(envvar)
    return envvar_values

def configmanager(config_path, settings):
    with open(os.path.join(config_path, 'config.yml'), 'r') as file:
        configuration = yaml.safe_load(file.read())
    for item in configuration['settings']:
        if item not in settings:
            settings[item] = configuration['settings'][item]

    return settings

def secretsmanager(dir, settings):
    secret_array = {}
    secretfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    for secret in secretfiles:
        with open(os.path.join(dir, secret), 'r') as file:
            data = file.read().replace('\n', '').replace('\r', '')
            if secret not in settings:
                settings[secret] = data

    return settings

def settings():
    settings = envvarmanager()

    secrets_path = os.getenv("CV_SECRETS_PATH", None)
    if secrets_path is not None:
        settings = secretsmanager(secrets_path, settings)

    config_path = os.getenv("CV_CONFIG_PATH", None)
    if config_path is not None:
        settings = configmanager(config_path, settings)
    return settings