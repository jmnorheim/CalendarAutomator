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

def create_event():
    service = authenticate()
    
    calendar_name = 'Jensern'
    calendar_id = get_calendar_id(service, calendar_name)
    if not calendar_id:
        print(f"Calendar '{calendar_name}' not found.")
        return
    
    events = [
        # Wednesday Lectures
        {
            'summary': '[Forelesning] - ML & Data Mining',
            'location': 'AULA V, Viale del Risorgimento, 4 - Bologna',
            'description': 'Room: AULA V',
            'start': {
                'dateTime': '2024-10-02T09:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-10-02T11:30:00',
                'timeZone': 'Europe/Rome',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;UNTIL=20241218T235959Z;BYDAY=WE',
                'EXDATE;TZID=Europe/Rome:20241009T090000,20241204T090000',
            ],
        },
        # Thursday Lectures
        {
            'summary': '[Forelesning] - ML & Data Mining',
            'location': 'AULA 2.3, Viale del Risorgimento, 2 - Bologna',
            'description': 'Room: AULA 2.3',
            'start': {
                'dateTime': '2024-10-03T15:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-10-03T17:00:00',
                'timeZone': 'Europe/Rome',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;UNTIL=20241219T235959Z;BYDAY=TH',
                'EXDATE;TZID=Europe/Rome:20241205T150000',
            ],
        },
        # Tuesday Lab Sessions
        {
            'summary': '[Lab Session] - ML & Data Mining',
            'location': 'LAB 9 and LAB 4, Viale del Risorgimento, 2 - Bologna',
            'description': 'Rooms: LAB 9 and LAB 4',
            'start': {
                'dateTime': '2024-10-22T12:00:00',
                'timeZone': 'Europe/Rome',
            },
            'end': {
                'dateTime': '2024-10-22T15:00:00',
                'timeZone': 'Europe/Rome',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;UNTIL=20241217T235959Z;BYDAY=TU',
            ],
        },
    ]
    
    for event in events:
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")

create_event()
