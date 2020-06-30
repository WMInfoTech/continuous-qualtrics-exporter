from msgraph import api, user, files
import os

def uploadtoonedrive(uploadfilepath, uploadfile, authority_host_uri, tenant, resource_uri, client_id, client_thumbprint
                     , client_cert, od_user, od_folder):
    try:
        upload_folder=None
        client_certificate_path = client_cert
        with open(client_certificate_path, 'rb') as input_file:
            client_certificate = input_file.read()

        api_instance = api.GraphAPI.from_certificate(authority_host_uri, tenant, resource_uri, client_id, client_certificate, client_thumbprint)

        test_user = user.User.get(api_instance, od_user)
        # fetch a OneDrive of a given user
        drive = files.Drive.get(api_instance, user=test_user)

        accessible_drives = files.Drive.accessible(api_instance, user=od_user)
        # print(accessible_drives)

        # fetch the root folder of the drive
        drive_root_folder = files.DriveItem.root_folder(api_instance, drive=drive)
        # print(drive_root_folder)
        # fetch children of the root directory of a drive
        root_children = files.DriveItem.get_children(api_instance, drive=drive)
        # fetch children of parent folder
        for child in root_children:
            if child.name == od_folder:
                upload_folder = child

        if upload_folder is None:
            print("Could not find the intended upload folder")
            exit(1)
        else:
            try:
                with open(os.path.join(uploadfilepath, uploadfile), 'rb') as input_file:
                    new_file = files.DriveItem.upload(api_instance, input_file.read(), drive=drive, parent=upload_folder, file_name=uploadfile)
                return "Success"
            except Exception as e:
                print(str(e))
                return "Failed"
            # print(new_file)
    except Exception as e:
        print("There was an error uploading to OneDrive")
        print(str(e))
        exit(1)

if __name__ == "__main__":
    from app.configmanager import settings

    try:
        settings = settings()

        uploadtoonedrive(settings['QUALTRICS_UPLOADPATH'], settings['QUALTRICS_UPLOADFILE'], settings['MS_AUTHORITY']
                         , settings['MS_TENANT'], settings['MS_RESOURCE'], settings['MS_CLIENTID']
                         , settings['MS_THUMBPRINT'], settings['MS_CLIENTCERT'], settings['MS_USER'],
                         settings['MS_USERFOLDER'])
    except Exception as e:
        print("There was an error while uploading to OneDrive")
        print(str(e))