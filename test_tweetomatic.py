import datetime
import unittest
import mock
from freezegun import freeze_time
from tweetomatic import time_to_event, select_event_data, NoEventsFound, create_tweet



# Mocks the current time to the below value
@freeze_time("2018-11-26 10:00")

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
            {'summary': 'test_summary', 'start': {'dateTime': '2018-11-23T21:00:00Z'},
             'end': {'dateTime': '2018-11-23T23:00:00Z'}}
            ]
    
        # act
        data_event = select_event_data(next_event)
        
        # assert
        self.assertEqual(data_event['summary'], 'test_summary')
        self.assertEqual(data_event['start'], datetime.datetime(2018, 11, 23, 21, 0, 0))
        self.assertEqual(data_event['end'], datetime.datetime(2018, 11, 23, 23, 0, 0))
        self.assertEqual(data_event['target_date'], datetime.date(2018, 11, 23))


"""


class TestSelectEvents(unittest.TestCase):
    @mock.patch("quickstart.get_calendar_events", mock.MagicMock(return_value=[]))
    def test_no_events(self):
        # act
        next_event = select_next_event()

        # assert
        self.assertEqual(next_event, None)

    @mock.patch("quickstart.get_calendar_events")
    def test_one_event_has_datetime(self, get_calendar_events):
        # arrange
        get_calendar_events.return_value = [
            {'summary': 'blah', 'start': {'dateTime': '2018-11-23T21:00:00Z'},
             'end': {'dateTime': '2018-11-23T23:00:00Z'}}]

        # act
        next_event = select_next_event()

        # assert
        self.assertEqual(next_event['summary'], 'blah')
        self.assertEqual(next_event['start'], datetime.datetime(2018, 11, 23, 21, 0, 0))
        self.assertEqual(next_event['end'], datetime.datetime(2018, 11, 23, 23, 0, 0))
        self.assertEqual(next_event['target_date'], datetime.date(2018, 11, 23))


class TestTimeToEvent(unittest.TestCase):
    
    def test_five_days_to_event(self):
        # arrange
        select_next_event.return_value = {'target_date': datetime.date(2018, 11, 28)}

        # act
        diff = time_to_event(data_event)

        # assert
        self.assertEqual(diff, -datetime.timedelta(days=5))

    def test_no_events(self):
        # arrange
        select_next_event.return_value = None

        # act/assert
        with self.assertRaises(NoEventsFound):
            time_to_event(data_event)


class TestCreateTweet(unittest.TestCase):
    def test_propagates_no_events_found_exception(self):
        # arrange
        data_event = {}
        diff = None
        time_to_event.side_effect = NoEventsFound

        # act/assert
        with self.assertRaises(NoEventsFound):
            create_tweet(data_event, diff)

    # test without mocking, directly passing parameters
    def test_has_correct_content(self):
        # arrange
        diff = datetime.timedelta(days=3)
        data_event = {
            'target_date': datetime.date(2018, 11, 28),
            'start': datetime.datetime(2018, 11, 28, 10, 30),
            'end': datetime.datetime(2018, 11, 28, 12, 0),
            'summary': 'FakeSummary'
            }

        # act
        tweet = create_tweet(data_event, diff)

        # assert
        self.assertEqual(tweet,
                         "The next FakeSummary will take place on "
                         "Wednesday, 28 November 2018, from 10.30 AM "
                         "to 12.00 PM. "
                         "Send us a DM on the day to receive a link to the private chat on "
                         "Telegram.")
"""

if __name__ == '__main__':
    unittest.main()


