from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate():
    creds = None
    credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def get_calendar_id(service, calendar_name):
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    for calendar in calendars:
        if calendar.get('summary') == calendar_name:
            return calendar.get('id')
    return None

def create_events():
    service = authenticate()
    
    calendar_name = 'Jensern'
    calendar_id = get_calendar_id(service, calendar_name)
    if not calendar_id:
        print(f"Calendar '{calendar_name}' not found.")
        return
    
    events = [
        # Event 1: Thursday Lectures (11:00 - 13:00)
        {
            'summary': '[Lecture] - Computer Vision and Image Processing M',
            'location': 'AULA 2.7B, Viale del Risorgimento, 2 - Bologna',
            'description': 'Teacher: Luigi Di Stefano',
            'start': {
                'dateTime': '2024-09-19T11:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-09-19T13:00:00',
                'timeZone': 'Europe/Rome',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;UNTIL=20241219T235959Z;BYDAY=TH',
            ],
        },
        # Event 2: Friday Lectures (14:00 - 17:00)
        {
            'summary': '[Lecture] - Computer Vision and Image Processing M',
            'location': 'AULA 2.7B, Viale del Risorgimento, 2 - Bologna',
            'description': 'Teacher: Luigi Di Stefano',
            'start': {
                'dateTime': '2024-10-11T14:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-10-11T17:00:00',
                'timeZone': 'Europe/Rome',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;UNTIL=20241220T235959Z;BYDAY=FR',
                'EXDATE;TZID=Europe/Rome:20241206T140000',
            ],
        },
        # Event 3: Friday Lecture with Different Location (27 Sep 2024)
        {
            'summary': '[Lecture] - Computer Vision and Image Processing M',
            'location': 'AULA 2.9, Viale del Risorgimento, 2 - Bologna',
            'description': 'Teacher: Luigi Di Stefano',
            'start': {
                'dateTime': '2024-09-27T14:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-09-27T17:00:00',
                'timeZone': 'Europe/Rome',
            },
        },
        # Event 4: Lab Sessions on Thursdays (09:00 - 11:00)
        {
            'summary': '[Lab Session] - Computer Vision and Image Processing M',
            'location': 'LAB 3, Viale del Risorgimento, 2 - Bologna',
            'description': 'Teacher: Luigi Di Stefano',
            'start': {
                'dateTime': '2024-10-03T09:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-10-03T11:00:00',
                'timeZone': 'Europe/Rome',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=6;BYDAY=TH',
                'EXDATE;TZID=Europe/Rome:20241031T090000',
            ],
        },
        # Event 5: Extended Lectures on Thursdays (09:00 - 12:00)
        {
            'summary': '[Lecture] - Computer Vision and Image Processing M (Extended Session)',
            'location': 'AULA 2.7B, Viale del Risorgimento, 2 - Bologna',
            'description': 'Teacher: Luigi Di Stefano',
            'start': {
                'dateTime': '2024-09-26T09:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-09-26T12:00:00',
                'timeZone': 'Europe/Rome',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;INTERVAL=2;COUNT=5;BYDAY=TH',
                'EXDATE;TZID=Europe/Rome:20241024T090000',
            ],
        },
    ]
    
    # Individual Extended Lectures (09:00 - 12:00) on 31 Oct, 14 Nov, 28 Nov
    additional_extended_lectures = [
        {
            'summary': '[Lecture] - Computer Vision and Image Processing M (Extended Session)',
            'location': 'AULA 2.7B, Viale del Risorgimento, 2 - Bologna',
            'description': 'Teacher: Luigi Di Stefano',
            'start': {
                'dateTime': '2024-10-31T09:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-10-31T12:00:00',
                'timeZone': 'Europe/Rome',
            },
        },
        {
            'summary': '[Lecture] - Computer Vision and Image Processing M (Extended Session)',
            'location': 'AULA 2.7B, Viale del Risorgimento, 2 - Bologna',
            'description': 'Teacher: Luigi Di Stefano',
            'start': {
                'dateTime': '2024-11-14T09:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-11-14T12:00:00',
                'timeZone': 'Europe/Rome',
            },
        },
        {
            'summary': '[Lecture] - Computer Vision and Image Processing M (Extended Session)',
            'location': 'AULA 2.7B, Viale del Risorgimento, 2 - Bologna',
            'description': 'Teacher: Luigi Di Stefano',
            'start': {
                'dateTime': '2024-11-28T09:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-11-28T12:00:00',
                'timeZone': 'Europe/Rome',
            },
        },
    ]
    
    events.extend(additional_extended_lectures)
    
    for event in events:
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")

create_events()
