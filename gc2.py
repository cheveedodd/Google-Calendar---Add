#! /usr/bin/python
# Google Calendar Add Event v0.1.1
# 2011 Chevee Dodd
"""Command line utility utilizing Google Calendar API."""

import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import base64
import time
import os


def load_credentials():
    """Get login information from credentials.cml.

    Future plans include passable argument to replace 'WORK' or a
    menu system for selecting different accounts.  Also - error
    handling.  CML = Credentials Markup Language - because I can."""
    with open('./data/credentials.cml', 'r') as f:
        line = f.readline()
        while line:
            if line.strip() == "WORK":
                username = f.readline()
                password = f.readline()
            line = f.readline()

    username = base64.b64decode(username)
    password = base64.b64decode(password)
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


def add_event(username, password, title, event_start, event_end):
    """Generate calendar event and send to Google

    This is ripped this straight from Google examples.  I'm sure it
    could be done differently.  The URLs are appended to the log file."""
    #build calendar service to pass to Google
    calendar_service = gdata.calendar.service.CalendarService()
    calendar_service.email = username
    calendar_service.password = password
    calendar_service.source = 'gc2.py'

    #build event data to pass to Google
    event = gdata.calendar.CalendarEventEntry()
    event.title = atom.Title(text=title)
    event.when.append(gdata.calendar.When(start_time=event_start, end_time=event_end))

    #log in to Google
    calendar_service.ProgrammaticLogin()

    # Send the request and receive the response
    new_event = calendar_service.InsertEvent(event, '/calendar/feeds/default/private/full')

    print 'New event added.  Check log file for link details.\n'
    # Build log as flat file for prosterity!
    with open('./data/work.log', 'a') as out_file:
        out_file.write('%s - %s\n' % (event_start, title))
        out_file.write('%s\n' % (new_event.id.text))
        out_file.write('%s\n' % (new_event.GetEditLink().href))
        out_file.write('%s\n\n' % (new_event.GetHtmlLink().href))


def first_run():
    print "This is your first time using Google Calendar Add Event."
    print "Let's set up the software by building your credentials file."
    print "\nWhen entering your email address, you must use your full login"
    print "address, including domain name.  ex: username@gmail.com"
    username = raw_input('Enter email > ')
    password = raw_input('Enter password > ')
    with open('./data/credentials.cml', 'w') as out_file:
        out_file.write('WORK\n')
        out_file.write('    %s\n' % (base64.b64encode(username)))
        out_file.write('    %s\n\n' % (base64.b64encode(password)))


def main():
    """Google Calendar Add  Event v0.1.1

    This utility is designed to add an event to Google Calendar with a
    minimal amount of effort.  User login information is stored in
    ./data/credentails.cml and is stored encoded with base64.  Calendar
    events are written to ./data/work.log as plain text.  See README"""
    if not os.path.exists('./data'):
        os.makedirs('./data')

    # Build Google login information
    username, password = load_credentials()

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
    add_event(username, password, input_title, event_start, event_end)


    print input_title, event_start, event_end
    print "\nEnd of line."


if __name__ == '__main__':
    if not os.path.exists('./data'):
        os.makedirs('./data')

    if not os.path.exists('./data/credentials.cml'):
        first_run()

    main()
