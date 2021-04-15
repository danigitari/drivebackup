import os
import os.path
import smtplib, ssl, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv, find_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaFileUpload


class Mydrive():
    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/drive']
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

    def list_files(self):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

    def upload_files(self, filename, path):
        load_dotenv(find_dotenv())
        folder_id = "1id5oAnyT0-P_kSHMs1-aRxk-qJIBeAR4"
        media = MediaFileUpload(f"{path}/{filename}")

        response = self.service.files().list(
                                        q=f"name='{filename}' and parents='{folder_id}'",
                                        spaces="drive",
                                        fields='nextPageToken,files(id,name)',
                                        pageToken=None).execute()
        if len(response['files']) == 0:
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"A new file was created {file.get('id')}")
        else:
            for file in response.get('files', []):
                update_file = self.service.files().update(
                    fileId=file.get('id'),
                    media_body=media,
                ).execute()
                print(f'updated file')
                print(update_file)
                port = 587  # For starttls
                smtp_server = "smtp.gmail.com"
                sender_email = os.getenv('SENDER_EMAIL')
                receiver_email = ""
                password = os.getenv('PASSWORD')
                msg = "The backup job for " + os.getenv('CLIENT_NAME') + " database has been successfuly executed and uploaded into Google Drive"
                error_msg = "The backup job for " + os.getenv('CLIENT_NAME') + " database has failed to upload to Google Drive. The error response was FILE NOT FOUND "
                message = MIMEMultipart()
                message["Subject"] = "Backup for " + os.getenv('CLIENT_NAME') + " success"
                message["From"] = sender_email
                message["To"] = receiver_email

                message.attach(MIMEText(msg, 'plain'))


                error_message = MIMEMultipart()
                error_message["Subject"] = "Backup for " + os.getenv('CLIENT_NAME') + " failed"
                error_message["From"] = sender_email
                error_message["To"] = receiver_email
                error_message.attach(MIMEText(error_msg, 'plain'))

                context = ssl.create_default_context()

                with smtplib.SMTP(smtp_server, port) as server:
                    server.ehlo()  # Can be omitted
                    server.starttls(context=context)
                    server.ehlo()  # Can be omitted
                    server.login(sender_email, password)
                    if update_file['mimeType'] == 'text/x-sql':
                        server.sendmail(sender_email, receiver_email, message.as_string())
                    else:
                        server.sendmail(sender_email, receiver_email, error_message.as_string())


def main():
    my_drive = Mydrive()
    path = os.path.abspath(__file__)
    files = os.listdir()
    dir_path = os.path.dirname(path)
    backup = 'danigitaridb.sql'
    join_path = os.path.join(dir_path, backup)
    backup_path = './danigitaridb.sql'
    if backup in files:
         my_drive.upload_files(backup, dir_path)
    else:
        print("error")

    # my_drive.upload_files(backup_path, join_path)


    # my_drive.upload_files(backup,join_path )
    # if backup in file:
    # join_path = os.path.join(dir_path)
    # my_drive.upload_files(backup, join_path)
    # else:
    #     print('file not found')
    # my_drive.list_files()
    # for items in file:
    #     my_drive.upload_files(items, join_path)


if __name__ == '__main__':
    main()

