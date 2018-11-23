from __future__ import print_function
from datetime import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from pprint import pprint
import tweepy

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


def get_calendar_events():
    """
    Calls the Calendar API and uses created token.json,
    which stores the user's access to access the google account.
    Puts next upcoming event in a json file.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events



def select_next_event():
    '''
    Selects the next event.
    Selects summary, date, start and end time of event and makes it readable.
    Saves data in a dictionary.
    '''
    events = get_calendar_events()
    if not events:
        # stop the function without error message
        print('No upcoming events found.')
        return

    event = events[0]
    summary = event['summary']
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    start_datetime = datetime.strptime(f'{start}', '%Y-%m-%dT%H:%M:%SZ')
    end_datetime = datetime.strptime(f'{end}', '%Y-%m-%dT%H:%M:%SZ')
    
    data_event = {'target_date': start_datetime.date(),
                  'summary': f'{summary}',
                  'start': start_datetime,
                  'end': end_datetime}
    
    pprint(data_event)
    return data_event


def time_to_event():
    '''
    Calculates and returns time from now to next event.
    '''
    data_event = select_next_event()
    if not data_event:
        raise NoEventsFound()
    print(data_event)
    now = datetime.now().date()
    target_date = data_event['target_date']
    diff = now - target_date
    return(diff)
    print(diff)

def format_date(dt):
    return datetime.strftime(dt, '%A, %d %B %Y')

def format_hour(dt):
    return datetime.strftime(dt, '%I.%M %p')

def create_tweet():
    '''
    If next event at a certain interval to now, returns tweet with data_event data.
    '''
    data_event = select_next_event()
    diff = time_to_event()
    
    # Add if function here:
    # if function comparing start_date with now:
        # if now - start_date <= 7:
            # create tweet
            # return tweet
        # now = datetime.utcnow().isoformat() + 'Z'

    tweet = f"The next {data_event['summary']} will take place" \
            + f" on {format_date(data_event['start'])}, from {format_hour(data_event['start'])}" \
            + f" to {format_hour(data_event['end'])}." \
            + f" Send us a DM on the day to receive a link to the private chat on Telegram."
    print(tweet)
    return tweet


def send_tweet(tweet):
    auth = tweepy.OAuthHandler("your_consumer_key", "your_consumer_key_secret")
    auth.set_access_token("your_access_token", "your_access_token_secret")
    api = tweepy.API(auth)
    api.update_status(tweet)


def main():
    get_calendar_events()
    select_next_event()
    time_to_event()
    try:
        tweet = create_tweet()
        send_tweet(tweet)
    except NoEventsFound:
        print("No events found")

# class EventNotInRange(Exception)

class NoEventsFound(Exception):
    pass


if __name__ == '__main__':
    main()

