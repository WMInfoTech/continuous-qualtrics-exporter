import os
from msgraph import api, user, files


def uploadtoonedrive(uploadfilepath, uploadfile, authority_host_uri, tenant, resource_uri, client_id, client_thumbprint
                     , client_cert, od_user, od_folder):
    try:
        client_certificate_path = client_cert
        with open(client_certificate_path, 'rb') as input_file:
            client_certificate = input_file.read()

        api_instance = api.GraphAPI.from_certificate(authority_host_uri, tenant, resource_uri, client_id, client_certificate, client_thumbprint)

        test_user = user.User.get(api_instance, od_user)
        # fetch a OneDrive of a given user
        drive = files.Drive.get(api_instance, user=test_user)

        accessible_drives = files.Drive.accessible(api_instance, user=od_user)
        print(accessible_drives)

        # fetch the root folder of the drive
        drive_root_folder = files.DriveItem.root_folder(api_instance, drive=drive)
        print(drive_root_folder)
        # fetch children of the root directory of a drive
        root_children = files.DriveItem.get_children(api_instance, drive=drive)
        # fetch children of parent folder
        for child in root_children:
            if child.name == od_folder:
                upload_folder = child

        with open(os.path.join(uploadfilepath, uploadfile), 'rb') as input_file:
            new_file = files.DriveItem.upload(api_instance, input_file.read(), drive=drive, parent=upload_folder, file_name=uploadfile)
    except Exception as e:
        print("There was an error uploading to OneDrive")
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

    if 'MICROSOFT_AUTHORITY' in secrets:
        MICROSOFT_AUTHORITY = secrets['MICROSOFT_AUTHORITY']
    else:
        MICROSOFT_AUTHORITY = os.getenv("MICROSOFT_AUTHORITY", None)

    if 'MICROSOFT_TENANT' in secrets:
        MICROSOFT_TENANT = secrets['MICROSOFT_TENANT']
    else:
        MICROSOFT_TENANT = os.getenv("MICROSOFT_TENANT", None)

    if 'MICROSOFT_RESOURCE' in secrets:
        MICROSOFT_RESOURCE = secrets['MICROSOFT_RESOURCE']
    else:
        MICROSOFT_RESOURCE = os.getenv("MICROSOFT_RESOURCE", None)

    if 'MICROSOFT_CLIENTID' in secrets:
        MICROSOFT_CLIENTID = secrets['MICROSOFT_CLIENTID']
    else:
        MICROSOFT_CLIENTID = os.getenv("MICROSOFT_CLIENTID", None)

    if 'MICROSOFT_THUMBPRINT' in secrets:
        MICROSOFT_THUMBPRINT = secrets['MICROSOFT_THUMBPRINT']
    else:
        MICROSOFT_THUMBPRINT = os.getenv("MICROSOFT_THUMBPRINT", None)

    if 'MICROSOFT_CERT' in secrets:
        MICROSOFT_CERT = secrets['MICROSOFT_CERT']
    else:
        MICROSOFT_CERT = os.getenv("MICROSOFT_CERT", None)

    if 'MICROSOFT_USER' in secrets:
        MICROSOFT_USER = secrets['MICROSOFT_USER']
    else:
        MICROSOFT_USER = os.getenv("MICROSOFT_USER", None)

    if 'MICROSOFT_USERFOLDER' in secrets:
        MICROSOFT_USERFOLDER = secrets['MICROSOFT_USERFOLDER']
    else:
        MICROSOFT_USERFOLDER = os.getenv("MICROSOFT_USERFOLDER", None)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--uploadPath", help="Upload file path")
    parser.add_argument("-f", "--uploadFile", help="Upload file name")
    parser.add_argument("-a", "--authority", help="Authority host URI", default=MICROSOFT_AUTHORITY)
    parser.add_argument("-t", "--tenant", help="Tenant", default=MICROSOFT_TENANT)
    parser.add_argument("-r", "--resource", help="Resource URI", default=MICROSOFT_RESOURCE)
    parser.add_argument("-c", "--cliendID", help="Resource URI", default=MICROSOFT_CLIENTID)
    parser.add_argument("-g", "--thumbPrint", help="Thumb Print", default=MICROSOFT_THUMBPRINT)
    parser.add_argument("-b", "--clientCert", help="Client certificate path and certificate filename", default=MICROSOFT_CERT)
    parser.add_argument("-u", "--msUser", help="Client certificate path and certificate filename", default=MICROSOFT_USER)
    parser.add_argument("-d", "--msUserFolder", help="Client certificate path and certificate filename", default=MICROSOFT_USERFOLDER)
    args = parser.parse_args()
    uploadtoonedrive(args.uploadPath, args.uploadFile, args.authority, args.tenant, args.resource, args.cliendID
                     , args.thumbPrint, args.clientCert, args.msUser, args.msUserFolder)