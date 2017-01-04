#!/usr/bin/env python
import argparse
import gspread
import logging
import os

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from sparkpost import SparkPost

# Grab important environment variables.
CLIENT_SECRET_FILE = os.getenv('RES_CREDS_FILENAME')
SPREADSHEET_ID = os.getenv('RES_SPREADSHEET_ID')

# gspread boilerplate
scope = ['https://spreadsheets.google.com/feeds']

# This is a workaround for keeping track of multiple sends per user in a
# spreadsheet. We use 1 column per send, and a send_id (1 indexed) to determine
# a bunch of other things for each send. This is the offset we add to send_id
# to determine which column we should be using for a particular send.
STATUS_COL_OFFSET = 8

# create logger
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('resolutions.log')
fh.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
log.addHandler(fh)
log.addHandler(ch)

# Give ability to set the "now" date from teh command line
argparser = argparse.ArgumentParser()
argparser.add_argument("--now", help="Set active 'curent' date for debugging")
args = argparser.parse_args()

def get_credentials():
    """ Do credentially things with google apps.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE, scope)
    gc = gspread.authorize(credentials)
    return gc

def get_resolution_data(sheet, send_id, tab_name="resolutions" ):
    """ returns a list of dictionaries, each the resolution data for a user,
        using the send_id value to determine which column we should use to track
        Sent status for this send.

        Also stuffs the original gpread row object in each dict so we can make
        updates later
    """
    wks = sheet.worksheet(tab_name)
    dictified_rows = []
    rowcounter = 2
    while True:
        row = wks.range("A{0}:N{0}".format(rowcounter))
        if row[0].value != '':
            rowdict = {
                "Timestamp": row[0].value,
                "Name": row[1].value,
                "Email": row[2].value,
                "Topic": row[6].value,
                "Resolution": row[7].value,
                "Sent": row[STATUS_COL_OFFSET + send_id].value,
                "original_row_cells": row
                }
            dictified_rows.append(rowdict)
            rowcounter += 1
        else:
            break
    return dictified_rows, wks

def get_dates(sheet, tab_name="dates"):
    """ Fetches date specific data so we can make decisions aorund it
    """
    wks = sheet.worksheet(tab_name)
    dictified_rows = []
    rowcounter = 2
    while True:
        row = wks.range("A{0}:E{0}".format(rowcounter))
        if row[0].value != '':
            rowdict = {
                "start": row[0].value,
                "end": row[1].value,
                "templateID": row[2].value,
                "send_id": row[4].value,
                }
            dictified_rows.append(rowdict)
            rowcounter += 1
        else:
            break
    return dictified_rows

def get_topic_data(sheet, tab_name="messages"):
    """ Returns a dictionary of Topic keys with a values containing
        relevent Phrase and Photoprefix k/v pairs for each
    """
    wks = sheet.worksheet(tab_name)
    rowdict = {}
    rowcounter = 2
    while True:
        row = wks.range("A{0}:C{0}".format(rowcounter))
        if row[0].value != '':
            rowdict[row[0].value] = {
                "Phrase": row[1].value,
                "Photoprefix": row[2].value,
                }
            rowcounter += 1
        else:
            break
    return rowdict

def get_sheet_connection(sheet_id):
    """ Gets a connection to the spreadsheet by sheet ID
    """
    gc = get_credentials()
    return gc.open_by_key(sheet_id)

def update_sent_flag_for_row(wks, row, fieldnum):
    """ Use the original gspread row object to access the
        cell objects to update the actual relevent cell's Sent
        status
    """
    row['original_row_cells'][fieldnum].value = "Sent"
    wks.update_cells(row['original_row_cells'])

def decypher_date(datestr):
    """ Turn 12/17/2016 style dates that Goodgle sheets gives us
        and convert into a datetime object
    """
    split = datestr.split('/')
    return datetime(int(split[2]), int(split[0]), int(split[1]))

def get_date_specifics(service, now):
    """ Figure out which "send" we're doing based
        on the date ranges in the dates worksheet
    """
    dates = get_dates(service)
    for date in dates:
        start = decypher_date(date['start'])
        end = decypher_date(date['end'])
        if start <= now:
            if end > now:
                return date['templateID'], int(date['send_id'])
            else:
                continue
        else:
            log.info("We haven't started yet!")
            exit(1)

def do_resolutions():
    """ This is where we do things
    """
    if args.now:
        now = decypher_date(args.now)
    else:
        now = datetime.now()

    log.info("Initiating run")

    sp = SparkPost()
    sheet_conn = get_sheet_connection(SPREADSHEET_ID)

    templateID, send_id = get_date_specifics(sheet_conn, now)
    resolution_data, resolution_sheet = get_resolution_data(sheet_conn, send_id)
    messages = get_topic_data(sheet_conn)

    if resolution_data:
        for row in resolution_data:
            if row['Sent'] != "Sent":
                log.info('Sending to %s, with %s' % (row['Email'], templateID))
                response = sp.transmissions.send(
                            recipients=[row['Email']],
                            campaign='resolutions'
                            template=templateID,
                            substitution_data={
                                'name': row['Name'],
                                'resolution_text': row['Resolution'],
                                'photo': "{}{}.jpg".format(messages[row['Topic']]['Photoprefix'], send_id),
                                'topic_phrase': messages[row['Topic']]['Phrase']
                            },
                            track_opens=True,
                            track_clicks=True
                            )
                success = response.get('total_accepted_recipients', 0)
                if success > 0:
                    update_sent_flag_for_row(resolution_sheet, row, send_id + STATUS_COL_OFFSET)
                    log.info("Success")
                else:
                    log.error("YOU FAIL, {} !".format(row['Email']))
                    log.error(response)
                    log.error("----------------------------------")
            else:
                log.debug("Already sent {} to {}, Skipping...".format(templateID, row['Email']))

    else:
        log.warn('No data found.')
    log.info("Finishing run")

if __name__ == '__main__':
    do_resolutions()
