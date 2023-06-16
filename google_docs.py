from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import psycopg2
from settings.base import get_secret
from db_commands import *

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

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
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()

        #Extract body
        body = document.get('body')
        lines = len(body['content'])

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