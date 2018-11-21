Tweetomatic

An application which takes information about events from google calendar and
tweets out reminders about them.

Complex version:
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
    
Simple version: 
    1. Create a file with all the dates and description and status
    2. Create a loop: while any event has a status less than 3, run function
    3. Access the file in read mode
    4. Determine current date with datetime
    5. Retrieve data with date at a specific time from “now”
    6. Retrieve that information and put it in a dictionary: date, description, status
    7. Put information into a string
    8. Print string
    9. Change status to 1, 2, 3
    10. Return dictionary with updated status
    11. Close file
    12. Open file in write mode
    13. Delete old table
    14. Put in new table with updated dictionary
