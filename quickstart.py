from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        summary = event['summary']
        start = datetime.datetime.strptime(f'{start}', '%Y-%m-%dT%H:%M:%SZ')
        end = datetime.datetime.strptime(f'{end}', '%Y-%m-%dT%H:%M:%SZ')
        print(datetime.datetime.strftime(start, f'The next {summary} will be on %d %B %Y from %I.%M -'), end = ' ')
        print(datetime.datetime.strftime(end, '%I.%M %p. Send us a DM on the day to receive a link to the private chat on Telegram.'))
        # pprint(events)


# time delta object: can be used to compare if one is bigger than the other

if __name__ == '__main__':
    main()
