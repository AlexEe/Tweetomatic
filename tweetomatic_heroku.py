from os import environ
import json

"""
Gets access environmental variables and puts them in variables.
Need to be imported before googleapiclient and twitter api client.
"""
credentials_json = environ.get("CREDENTIALS_JSON")
token_json = environ.get("TOKEN_JSON")
twitter_access_token = environ.get("TWITTER_ACCESS_TOKEN")
twitter_api_key = environ.get("TWITTER_API_KEY")
env_var = True


def write_env_to_json(content, filename):    
    """
    Takes environmental variables and turns them into .json files.
    Needs to be called before importing googleapiclient.
    Changes env_var to False if env variables have not been set.
    """
    global env_var
    try:
        with open(filename, "w") as f:
            f.write(content)
    except TypeError:
        env_var = False
        return env_var
        
        
"""
Creates .json files with contents of env variables,
to be used by google api client and twitter api client.
"""
credentials = write_env_to_json(credentials_json, "credentials.json")
token = write_env_to_json(token_json, "token.json")
twitter_token = write_env_to_json(twitter_access_token, "twitter_access_token.json")
twitter_api = write_env_to_json(twitter_api_key, "twitter_api_key.json")


from datetime import datetime, timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import tweepy
import sys



def get_next_event(env_var):
    """
    If env variables available:
    Calls the Google Calendar API with token.json, and credentials.json,
    which store the user's secret access tokens and keys.
    Selects next upcoming event from calendar.
    """
    if env_var == False:
        raise NoEnvVariables(Exception)

    SCOPES = "https://www.googleapis.com/auth/calendar.readonly"

    store = file.Storage("token.json")
    creds = store.get()
    
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
        
    service = build("calendar", "v3", http=creds.authorize(Http()))
    now = datetime.utcnow().isoformat() + "Z" # "Z" indicates UTC time
    events_result = service.events().list(calendarId="primary", timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy="startTime").execute()
    next_event = events_result.get("items", [])
    return next_event


def select_event_data(next_event):
    """
    Selects summary, turns start and end into datetime objects,
    creates target_date as datetime.date object, formated for scheduling.
    Saves data in a dictionary.
    """
    if not next_event:
        raise NoEventsFound(Exception)

    event = next_event[0]
    summary = event["summary"]
    start = event["start"].get("dateTime", event["start"].get("date"))
    end = event["end"].get("dateTime", event["end"].get("date"))
    start_datetime = datetime.strptime(f"{start}", "%Y-%m-%dT%H:%M:%SZ")
    end_datetime = datetime.strptime(f"{end}", "%Y-%m-%dT%H:%M:%SZ")
    
    data_event = {"target_date": start_datetime.date(),
                  "summary": f"{summary}",
                  "start": start_datetime,
                  "end": end_datetime
                  }
    return data_event


        
def time_to_event(data_event):
    """
    Calculates and returns time from now to next event.
    """
    if not data_event:
        raise NoDataFound(Exception)
    
    now = datetime.now().date()
    target_date = data_event["target_date"]
    diff = now - target_date
    #print(diff)
    return(diff)


def format_date(dt):
    """
    Function to format datetime object as string: weekday, day, month, year.
    """
    return datetime.strftime(dt, "%A, %d %B %Y")


def format_date_short(dt):
    return datetime.strftime(dt, "%d %B")


def format_weekday(dt):
    return datetime.strftime(dt, "%A")


def format_hour(dt):
    """
    Function to format datetime object as string: hour, minute, AM/PM.
    """
    return datetime.strftime(dt, "%I.%M %p")


def create_tweet(data_event, diff):
    """
    If next event at a certain interval to now, returns tweet.
    """
    summary = data_event["summary"]
    date_month_year = format_date(data_event["start"])
    weekday = format_weekday(data_event["start"])
    start_hour = format_hour(data_event["start"])
    end_hour = format_hour(data_event["end"])
    date_month = format_date_short(data_event["start"])

    if diff == timedelta(days=-7):
        tweet = f"Our next {summary} will take place" \
                + f" on {date_month_year}, from {start_hour}" \
                + f" to {end_hour}." \
                + " Send us a DM on the day to receive a link to the private chat on Telegram."

        return tweet

    elif diff == timedelta(days=-4):
        tweet = "Join our bi-weekly chat on Telegram" \
                + f" next {weekday} ({start_hour} to {end_hour})," \
                + " a private and safe get-together for bi survivors" \
                + " of all genders! :)"

        return tweet
    
    elif diff == timedelta(days=-2):
        tweet = "As always, you can receive the secret link to our chat" \
                + f" this {weekday}, {start_hour} to {end_hour} by sending us a DM!" \
                + " Make sure to download Telegram" \
                + " in advance so you're ready!"

        return tweet

    elif diff == timedelta(days=-1):
        tweet = "Let us know how you're doing at our bi-weekly chat on Telegram," \
                + f" tomorrow at {start_hour}." \
                + " As always, the chat is moderated by a non-monosexual survivor."           

        return tweet

    elif diff == timedelta(days=-0):
        tweet = "Last minute reminder! Our chat for bi survivors is" \
                + f" going live tonight from {start_hour} to {end_hour}." \
                + " Send us a DM now to" \
                + " receive the secret link to the chat on Telegram."

        return tweet

    else:
        raise EventNotInRange(Exception)
    

def send_tweet(tweet):
    """
    Opens json file with access tokens and twitter api keys.
    Checks length of tweet, if over 240 raises error.
    Otherwise, publishes tweet on timeline.
    """
    with open ("twitter_access_token.json", "r") as f:
        tokens = json.load(f)
        access_token = tokens["access_token"]
        access_token_secret = tokens["access_token_secret"]
        
    with open ("twitter_api_key.json", "r") as f:
        keys = json.load(f)
        api_key = keys["api_key"]
        api_secret_key = keys["api_secret_key"]

    auth = tweepy.OAuthHandler(f"{api_key}", f"{api_secret_key}")
    auth.set_access_token(f"{access_token}", f"{access_token_secret}") 
    api = tweepy.API(auth)

    if len(tweet) > 240:
        raise TweetTooLong(Exception)

    else:
        #print(tweet)
        api.update_status(tweet) # Uncomment to send tweet


def main():
    try:
        next_event = get_next_event(env_var)
    except NoEnvVariables:
        sys.exit("No environmental variables.")
    data_event = select_event_data(next_event)
    diff = time_to_event(data_event)
    try:
        tweet = create_tweet(data_event, diff)
        send_tweet(tweet)
    except NoEventsFound:
        print("No events found.")
    except NoDataFound:
        print("No data passed into data_event dictionary.")
    except EventNotInRange:
        print("Event is not in range.")
    except TweetTooLong:
        print("Tweet has over 240 characters.")


class EventNotInRange(Exception):
    pass

class NoEventsFound(Exception):
    pass

class NoDataFound(Exception):
    pass

class TweetTooLong(Exception):
    pass

class NoEnvVariables(Exception):
    pass


if __name__ == "__main__":
    main()

