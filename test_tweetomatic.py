import datetime
from datetime import timedelta
import unittest
import mock
import json
import tweepy
from freezegun import freeze_time
from tweetomatic_heroku import time_to_event, select_event_data, format_date, format_date_short, format_hour, NoDataFound, NoEventsFound, EventNotInRange, create_tweet


class TestSelectEventData(unittest.TestCase):
    
    def test_no_events_raises_NoEventsFound(self):
        # act
        next_event = []

        # assert
        with self.assertRaises(NoEventsFound):
            select_event_data(next_event)

    
    def test_returns_event_data(self):
        # arrange
        next_event = [
            {'summary': 'test summary', 'start': {'dateTime': '2018-11-23T21:00:00Z'},
             'end': {'dateTime': '2018-11-23T23:00:00Z'}}
            ]
    
        # act
        data_event = select_event_data(next_event)
        
        # assert
        self.assertEqual(data_event['summary'], 'test summary')
        self.assertEqual(data_event['start'], datetime.datetime(2018, 11, 23, 21, 0, 0))
        self.assertEqual(data_event['end'], datetime.datetime(2018, 11, 23, 23, 0, 0))
        self.assertEqual(data_event['target_date'], datetime.date(2018, 11, 23))


@freeze_time("2018-11-23 10:00")
class TestTimeToEvent(unittest.TestCase):

    def test_no_events_found_raises_NoDataFound(self):
        # act
        data_event = {}

        # assert
        with self.assertRaises(NoDataFound):
            time_to_event(data_event)

    def test_returns_correct_diff(self):
        # arrange
        target_date = datetime.date(2018, 11, 28)
        now = datetime.datetime.now().date()

        # act
        diff = now - target_date

        # assert
        self.assertEqual(diff, -datetime.timedelta(days=5))


class TestFormatDate(unittest.TestCase):

    def test_returns_formated_date(self):
        # arrange
        example_date = datetime.datetime(2018, 11, 23, 21, 0, 0)

        # act
        formated_date = format_date(example_date)

        # assert
        self.assertEqual(formated_date, "Friday, 23 November 2018")


class TestFormatDateShort(unittest.TestCase):

    def test_returns_date_month(self):
        # arrange
        example_date = datetime.datetime(2018, 11, 23, 21, 0, 0)

        # act
        formated_date = format_date_short(example_date)

        # assert
        self.assertEqual(formated_date, "23 November")


class TestFormatHour(unittest.TestCase):
    
    def test_returns_start_hour(self):
        # arrange
        example_date = datetime.datetime(2018, 11, 23, 21, 0, 0)

        # act
        formated_date = format_hour(example_date)

        # assert
        self.assertEqual(formated_date, "09.00 PM")        


class TestCreateTweet(unittest.TestCase):
    
    def test_raises_EventNotInRange_exception(self):
        # arrange
        data_event = {"summary": "test summary",
                      "start": datetime.datetime(2018, 11, 23, 21, 0, 0),
                      "end": datetime.datetime(2018, 11, 23, 23, 0, 0),
                      "target_date": datetime.date(2018, 11, 23)
                      }
        diff = timedelta(days=-9)

        # act/ assert
        with self.assertRaises(EventNotInRange):
            create_tweet(data_event, diff)
            


    def test_returns_formated_tweet(self):
        # arrange
        data_event = {"summary": "test summary",
                      "start": datetime.datetime(2018, 11, 23, 21, 0, 0),
                      "end": datetime.datetime(2018, 11, 23, 23, 0, 0),
                      "target_date": datetime.date(2018, 11, 23)
                      }

        diff = timedelta(days=-7)
        
        # act
        tweet = create_tweet(data_event, diff)

        # assert
        self.assertEqual(tweet, "Our next test summary will take place" \
                + " on Friday, 23 November 2018," \
                + " from 09.00 PM to 11.00 PM." \
                + " Send us a DM on the day to receive a link to the private chat on Telegram.")


class TestTwitterAccess(unittest.TestCase):

    def test_twitter_returns_last_twenty_tweets(self):

        # arrange
        with open("twitter_access_token.json", "r") as f:
            tokens = json.load(f)
            access_token = tokens["access_token"]
            access_token_secret = tokens["access_token_secret"]
        with open("twitter_api_key.json", "r") as f:
            keys = json.load(f)
            api_key = keys["api_key"]
            api_secret_key = keys["api_secret_key"]
            
        auth = tweepy.OAuthHandler(f"{api_key}", f"{api_secret_key}")
        auth.set_access_token(f"{access_token}", f"{access_token_secret}") 
        api = tweepy.API(auth)

        # act
        public_tweets = api.home_timeline()
        tweet = 0
        for i in public_tweets:
            tweet += 1

        # assert
        self.assertEqual(tweet, 20)



if __name__ == '__main__':
    unittest.main()


