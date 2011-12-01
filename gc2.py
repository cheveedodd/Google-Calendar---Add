#! /usr/bin/python
# Google Calendar Add Event v0.1.2
# This code runs against Google Calendar API v2.1 which is deprecated
# as of 11/4/2011 - use with caution.
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
import sys
import getpass


def load_credentials(account='WORK'):
    """Get login information from file and return username/password.

    arguments:
    account -- user defined name for credential set (default: WORK)
    """
    with open('./data/credentials.cml', 'r') as f:
        line = f.readline()
        while line:
            if line.strip() == account:
                username = f.readline()
                password = f.readline()
            line = f.readline()

    username = base64.b64decode(username)
    password = base64.b64decode(password)
    return username, password


def get_title():
    """Get calendar Title from user return string.

    Format as raw to allow time and date in Google event title.
    """
    title = ''
    while (title == ''):
        title = raw_input('Title? > ')

    return title


def get_date():
    """Get date from user return string.

    Input format must be yyyy-mm-dd
    Return current date if nothing is entered.

    Future plans are to include functions to parse various formats
    instead of a forced format.  I like Googles quick-add parsing but
    it prevents me from puting dates or times in the event title
    without enclosing it in quotes - which would be fine if the quotes
    were stripped out by the quick-add function.
    """
    input_day = raw_input('Day? YYYY-MM-DD [Today] > ')

    if not input_day:
        input_day = time.strftime('%Y-%m-%d')

    return input_day


def get_time():
    """Get time information from user.  Return two strings.

    Input format must be either HH:MM:SS or HH:MM
    Return empty if nothing is entered.
    """
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
    """Generate calendar event and send to Google.

    arguments:
    username -- fully qualified address eg username@domain.com as string
    password -- password as string
    title -- event title as string
    event_start -- starting date/time as string YYYY-mm-ddTHH:mm:ss
    event_end -- ending date/time as string YYYY-mm-ddTHH:mm:ss
    """
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


def add_user(reason, account='WORK'):
    """Add user to credentials file.

    arguments:
    reason -- additional instructions passed to user as string
    account -- user defined name for credential set (default: WORK)

    Currently this module builds the credentials file for only a single
    login/password pair if rain against a previously built file it will
    overwrite any data in that file.
    """
    print reason
    print "When entering your email address, you must use your full login"
    print "address, including domain name.  ex: username@gmail.com"
    username = raw_input('Enter email > ')

    password = ''
    while not password:
        first_pass = getpass.getpass('Enter password > ')
        second_pass = getpass.getpass('Re-enter password > ')
        if first_pass == second_pass:
            password = first_pass
        else:
            print 'Password missmatch.'

    with open('./data/credentials.cml', 'w') as out_file:
        out_file.write(account)
        out_file.write('\n    %s\n' % (base64.b64encode(username)))
        out_file.write('    %s\n\n' % (base64.b64encode(password)))


def main():
    """Google Calendar Add  Event v0.1.2

    This utility is designed to add an event to Google Calendar with a
    minimal amount of effort.  User login information is stored in
    ./data/credentails.cml and is stored encoded with base64.  Calendar
    events are written to ./data/work.log as plain text.  See README
    """
    #Get Google login information from file
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
        add_user('''This is the first time you've run Google Calendar Add Event.
Let's set up the software by building your credentials file.\n''')

    main()
