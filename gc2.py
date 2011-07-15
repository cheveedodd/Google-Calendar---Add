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

def gInfo():
    # Get login information from log file
    #
    # future plans include passable argument to replace 'work.log' or
    # a menu system for selecting calendars.  Also - error handling
    in_File = open('./data/work.log', 'r')
    a_Email = in_File.readline()
    a_Pass = in_File.readline()
    in_File.close()
    return a_Email, a_Pass

def gTitle():
    # Get calendar Title from user
    # Format as raw to allow time and date entry.
    a_Title = ''
    while (a_Title == ''):
        a_Title = raw_input('Title? > ')

    return a_Title

def gDate():
    # Get date from user
    # Format as yyyy-mm-dd
    # Return current date if nothing is entered.
    #
    # Future plans are to include functions to parse various formats
    # instead of a forced format.  I like Googles quick-add parsing but
    # it prevents me from puting dates or times in the event title
    # without enclosing it in quotes - which would be fine if the quotes
    # were stripped out by the quick-add function.
    a_Day = raw_input('Day? YYYY-MM-DD [Today] > ')

    while (a_Day == ""):
        a_Day = "%s-%s-%s" % (str(time.strftime('%Y')), str(time.strftime('%m')), str(time.strftime('%d')))

    return a_Day

def gTime():
    # Get time from user
    # Format as HH:MM:SS
    # Return empty if nothing is entered.
    #
    # Future plans are automatic parsing of different input formats.
    print 'Enter times in 24 hour format: HHmm'
    s_Time = raw_input('Start time? [All day] > ')
    if s_Time == '':
        return ''
    else:
        e_Time = raw_input('End time? > ')

    #convert input to HH:mm:ss
    s_Time = '%s:%s:00' % (s_Time[:2], s_Time[2:])
    e_Time = '%s:%s:00' % (e_Time[:2], e_Time[2:])

    a_Time = '%s %s' % (s_Time, e_Time)
    return a_Time

def gAdd(calendar_service, title, start_time, end_time):
	# I ripped this straight from Google examples
    # I'm sure it could be done differently.
    event = gdata.calendar.CalendarEventEntry()
    event.title = atom.Title(text=title)
    event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
    calendar_service.ProgrammaticLogin()

    # Send the request and receive the response:
    new_event = calendar_service.InsertEvent(event, '/calendar/feeds/default/private/full')

    print 'New event added.  Check log file for link details.\n'
    # Build log as flat file for prosterity!
    out_File = open('./data/work.log', 'a')
    out_File.write('%s - %s\n' % (start_time, title))
    out_File.write('%s\n' % (new_event.id.text))
    out_File.write('%s\n' % (new_event.GetEditLink().href))
    out_File.write('%s\n' % (new_event.GetHtmlLink().href))
    out_File.write('\n')
    out_File.close()


# This is where some sort of MAIN function should begin.  I know that I
# am supposed to use that, but I've never bothered to learn how.

# Build Google login information
a_Creds = gInfo()
calendar_service = gdata.calendar.service.CalendarService()
calendar_service.email = base64.b64decode(a_Creds[0])
calendar_service.password = base64.b64decode(a_Creds[1])
calendar_service.source = 'gc2.py'

#Get calendar information from user
print '\n\n\nGoogle Calendar Add Event:\n'
xTitle = str(gTitle())
xDate = str(gDate())
rTime = str(gTime())
if rTime > "":
    xTime = rTime.split()
    sTime = "%sT%s" % (xDate, str(xTime[0]))
    eTime = "%sT%s" % (xDate, str(xTime[1]))
else:
    sTime = xDate
    eTime = xDate

#Add calendar event
gAdd(calendar_service, xTitle, sTime, eTime)


print xTitle, sTime, eTime
print "\nEnd of line."
