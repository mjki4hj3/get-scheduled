from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
        
        n = datetime.datetime.now(datetime.timezone.utc)
        
        n_later = n + datetime.timedelta(hours=1)
        
        n = n.isoformat()
        n_later = n_later.isoformat()
        
        print('event start time:' + n)
        print('event end time:' + n_later)
        
        
        event = {
        'summary': 'Test',
        'location': '10 Downing Street, London',
        'description': 'A test calendar event',
        'start': {
            'dateTime': n,
            'timeZone': 'Europe/London'
        },
        'end': {
            'dateTime': n_later,
            'timeZone': 'Europe/London'            
        }
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()