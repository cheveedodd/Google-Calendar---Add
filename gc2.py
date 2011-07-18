#! /usr/bin/python
# Google Calendar Command Line Quick-Add v0.1.0
# 2011 Chevee Dodd
"""Command line utility utilizing Google Calendar API."""

import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import base64
import time

def load_credentials():
    """Get login information from log file.

    Future plans include passable argument to replace 'work.log' or
    a menu system for selecting calendars.  Also - error handling"""
    in_File = open('./data/work.log', 'r')
    username = in_File.readline()
    password = in_File.readline()
    in_File.close()
    return username, password

def get_title():
    """Get calendar Title from user.

    Format as raw to allow time and date entry."""
    title = ''
    while (title == ''):
        title = raw_input('Title? > ')

    return title

def get_date():
    """Get date from user

    Input format must be yyyy-mm-dd
    Return current date if nothing is entered.

    Future plans are to include functions to parse various formats
    instead of a forced format.  I like Googles quick-add parsing but
    it prevents me from puting dates or times in the event title
    without enclosing it in quotes - which would be fine if the quotes
    were stripped out by the quick-add function."""
    input_day = raw_input('Day? YYYY-MM-DD [Today] > ')

    if not input_day:
        input_day = time.strftime('%Y-%m-%d')

    return input_day

def get_time():
    """Get time from user

    Input format must be either HH:MM:SS or HH:MM
    Return empty if nothing is entered.

    Future plans are automatic parsing of different input formats."""
    print 'Enter times in 24 hour format: HHmm'
    start_time = raw_input('Start time? [All day] > ')
    if not start_time:
        return '', ''
    else:
        end_time = raw_input('End time? > ')

    #convert input to HH:mm:ss
    start_time = '%s:%s:00' % (start_time[:2], start_time[2:])
    end_time = '%s:%s:00' % (end_time[:2], end_time[2:])

    return start_time, end_time

def add_event(calendar_service, title, event_start, event_end):
    """Generate calendar event and send to Google

    This is ripped this straight from Google examples.  I'm sure it
    could be done differently.  The URLs are appended to the log file
    containing the user data."""
    event = gdata.calendar.CalendarEventEntry()
    event.title = atom.Title(text=title)
    event.when.append(gdata.calendar.When(start_time=event_start, end_time=event_end))
    calendar_service.ProgrammaticLogin()

    # Send the request and receive the response:
    new_event = calendar_service.InsertEvent(event, '/calendar/feeds/default/private/full')

    print 'New event added.  Check log file for link details.\n'
    # Build log as flat file for prosterity!
    out_File = open('./data/work.log', 'a')
    out_File.write('%s - %s\n' % (event_start, title))
    out_File.write('%s\n' % (new_event.id.text))
    out_File.write('%s\n' % (new_event.GetEditLink().href))
    out_File.write('%s\n' % (new_event.GetHtmlLink().href))
    out_File.write('\n')
    out_File.close()

def main():
    """Google Calendar Quick v0.1.0

    This utility is designed to add an event to Google Calendar with a
    minimal amount of effort.  User login information is stored in a
    log file with base64 encoding and is retreived with the program is
    executed.  This file must be in ./data and named work.log.  The
    first line must contain the users email and the second line must
    contain the users password.  Both must be encoded in base64."""
    # Build Google login information
    a_Creds = load_credentials()
    calendar_service = gdata.calendar.service.CalendarService()
    calendar_service.email = base64.b64decodehttp://www.yahoo.com/(a_Creds[0])
    calendar_service.password = base64.b64decode(a_Creds[1])
    calendar_service.source = 'gc2.py'

    #Get calendar information from user
    print '\n\n\nGoogle Calendar Add Event:\n'
    input_title = get_title()
    input_date = get_date()
    start_time, end_time = get_time()
    if not start_time:
        event_start = input_date
        event_end = input_date
    else:
		event_start = "%sT%s" % (input_date, start_time)
		event_end = "%sT%s" % (input_date, end_time)

    #Add calendar event
    add_event(calendar_service, input_title, event_start, event_end)


    print input_title, event_start, event_end
    print "\nEnd of line."


if __name__ == '__main__':
    main()
