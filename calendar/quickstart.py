from __future__ import print_function

import datetime
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


sys.path.append(os.path.dirname(__file__) + "..")
from app import app
df = app.prepare_dataframe()

SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
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
                '../credentials.json', SCOPES, redirect_uri='http://localhost:5000/')
            creds = flow.run_local_server(port=5000)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        
        events = []
        index=0
        print(len(df))
        while index < len(df):
            study_event = {
                'summary': df.loc[index, 'Name'],
                'description': df.loc[index, 'Name'],
                'start': {
                    #Convert from timestamps datatype to datetime object, add local timezone and then
                    # convert to required format
                    'dateTime': df.loc[index, 'Start Time'].to_pydatetime().astimezone().isoformat()
                },
                'end': {
                    'dateTime': df.loc[index, 'End Time'].to_pydatetime().astimezone().isoformat()     
                    }
            }
            if index+1 < len(df):
                if df.loc[index+1, 'Pomodoro Session'] - df.loc[index, 'Pomodoro Session'] > 0:
                    break_event = {
                        'summary': 'Pomodoro Break',
                        'description': 'Pomodoro Break',
                        'start': {
                            'dateTime': df.loc[index, 'End Time'].to_pydatetime().astimezone().isoformat()
                        },
                        'end': {
                            'dateTime': df.loc[index, 'Break Time'].to_pydatetime().astimezone().isoformat()     
                            },
                        'colorId': 2
                    }
                    events.append(break_event)
            
            events.append(study_event)            
            index += 1
        
        
        for event in events:
            event_item = service.events().insert(calendarId='primary', body=event).execute()
        
        print ('Event created: %s' % (event_item.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()