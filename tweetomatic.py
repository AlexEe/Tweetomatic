'''
Tweetomatic: Tweets reminders about Google Calendar events

Steps:
1. Access information from google calendar
2. Select the right kind of event: select by keyword “chat”
3. Get information into python: date, event name, description (skip if no description)
4. Put into a list/ dictionary
5. Create a function that creates strings with events, max 240 chars
6. Determine curent date and compare with date of event
7. Build a twitter bot 
8. Feed bot with created tweet and time depending on current date 
9. Put this information into a tweet
10. Write a twitter bot that is fed with the created tweet
11. Determine curent date and compare with date of event
12. Time the tweet depending on current date
13. Where do you host it: Heroku scheduler/ stackcp
'''

import gtk
import pynotify
pynotify.init(sys.argv[0])

calendar_service = gdata.calendar.service.CalendarService()
calendar_service.email = ''
# Potentially use OAuth 2.0 to make secure
calendar_service.password = ''
calendar_service.ProgrammaticLogin()

feed = calendar_service.GetCalendarEventFeed()
