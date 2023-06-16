from __future__ import print_function

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import psycopg2
from settings.base import get_secret
from db_commands import *
from utils import *
import requests
from oauth2client import file as f, client, tools
from httplib2 import Http

import os

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.metadata']

# The ID of a sample document.
DOCUMENT_ID = '13Ztp08sngMZ6ScMFu2YZNwXWOguEmVmVdbooLAVd-9k'


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('config/token.json'):
        creds = Credentials.from_authorized_user_file('config/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'config/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('config/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('docs', 'v1', credentials=creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=DOCUMENT_ID).execute()
        print('The title of the document is: {}'.format(document.get('title')))

        #Extract DB details from secrets
        HOST = get_secret('host')
        DATABASE = get_secret('database')
        USER = get_secret('user')
        PASSWORD = get_secret('password')
        
        #Establish db connection
        conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD)

        cur = conn.cursor()

        #Create table 'information'
        cur.execute(create_table_command)

        cur.execute(get_latest_row_command)
        fetch_all = cur.fetchall()
        latest_row = ''
        if len(fetch_all)!=0:
            latest_row = cur.fetchall()[0]
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()

        #Extract body
        body = document.get('body')
        lines = len(body['content'])
        
        store = f.Storage('config/credentials.json')
        # creds = Credentials.from_authorized_user_file('config/token.json', SCOPES)
        creds = None
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('config/credentials.json', scope=SCOPES)
            creds = tools.run_flow(flow, store)
        DRIVE = build('drive','v3', http=creds.authorize(Http()))

        files = DRIVE.files().get(fileId=DOCUMENT_ID, fields='*').execute()

        LATEST_USER_EMAIL = files['lastModifyingUser']['emailAddress']
        # START_TIME = files['createdTime']
        # MODIFIED_TIME = files['modifiedTime']
        
        ID = auto_fill_id(latest_row)
        CREATED = get_current_datetime()

        for i in range(lines):
            content = body['content'][i]

            #Get body content
            if 'paragraph' in content:
                #Check if the line contains text
                if 'textRun' in content['paragraph']['elements'][0]:
                    #Skip the extra end line(s)
                    if content['paragraph']['elements'][0]['textRun']['content'] =='\n':
                        continue
                    print(content['paragraph']['elements'][0]['textRun']['content'])


        
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()