#! /usr/bin/python
# Google Calendar Get Event v0.0.1
# 2011 Chevee Dodd
#
# This is a temporary module to test the event query code.  I repurposed
# the original Event adding module for this purpose.  This will be
# eventually merged with the Add Event module.

"""Command line utility utilizing Google Calendar API."""

import gdata.calendar.service
import gdata.calendar.client
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

def get_date(date_request):
    """Get date from user return string.

    Input format must be yyyy-mm-dd
    Return current date if nothing is entered.

    arguments:
    date_request -- String containing date request reason
    """
    input_day = raw_input(date_request + ' Date? YYYY-MM-DD [Today] > ')

    if not input_day:
        input_day = time.strftime('%Y-%m-%d')

    return input_day

def get_event(username, password, file_name, start_date, end_date):
    """Get calendar events from Google.

    arguments:
    username -- fully qualified address eg username@domain.com as string
    password -- password as string
    start_date -- starting date as string YYYY-mm-dd
    end_dater -- ending date as string YYYY-mm-dd
    """
    #build calendar service to pass to Google
    calendar_service = gdata.calendar.service.CalendarService(source='gcg.py')

    #log in to Google
    calendar_service.ClientLogin(username, password, calendar_service.source)

    #build event data to pass to Google
    query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full')
    query.start_min = start_date
    query.start_max = end_date
    query.max_results = 60
    print 'Date range query for events: %s to %s' % (start_date, end_date,)

    # Send the request and receive the response
    feed = calendar_service.CalendarQuery(query)
    print 'Events on Primary Calendar: %s' % (feed.title.text,)
    for i, an_event in enumerate(feed.entry):
        print '\t%s. %s' % (i, an_event.title.text,)
        for a_when in an_event.when:
            print '\t\tStart time: %s' % (a_when.start_time,)
            print '\t\tEnd time:   %s' % (a_when.end_time,)

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
    """Google Calendar Get  Event v0.0.1

    This utility is designed to add get events from Google Calendar
    within a specified date range.  User login information is stored in
    ./data/credentails.cml and is stored encoded with base64.  Output
    can be sent to a specified file or standard outuput.
    """
    #Get Google login information from file
    username, password = load_credentials()

    #Get calendar information from user
    print '\n\n\nGoogle Calendar Get Event:\n'
    start_date = get_date('Starting')
    end_date = get_date('Ending')

    file_name = './events.txt'

    #Add calendar event
    get_event(username, password, file_name, start_date, end_date)



    print "\nEnd of line."


if __name__ == '__main__':
    if not os.path.exists('./data'):
        os.makedirs('./data')

    if not os.path.exists('./data/credentials.cml'):
        add_user('''This is the first time you've run Google Calendar Get Event.
Let's set up the software by building your credentials file.\n''')

    main()
