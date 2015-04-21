#!/usr/bin/evn python2

__author__ = 'apinchuke'

import sys
import logging
import mysql.connector as connector
import config
import csv
from datetime import datetime

# This is a file that is to be converted into a database
CSV_PATH = sys.argv[1]
CSV_FILE = None
CURRENT_LINE = None
CURSOR = None
DB_NAME = 'assets'

# Show ALL the debug info by default
logging.basicConfig(level=logging.DEBUG)


logging.info('The file to process: %s', CSV_PATH)

CSV_FILE = open(CSV_PATH)
CURRENT_LINE = CSV_FILE.readline()
logging.info('The current line: %s', CURRENT_LINE)
CONNECTION = None

logging.debug('The user to be logged in: %s', config.database['user'])


CONNECTION = connector.connect(**config.database)
CURSOR = CONNECTION.cursor()
logging.debug('The current DB user is: %s', CONNECTION.user)


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


create_database(CURSOR)
CONNECTION = connector.connect(user=config.database['user'], database=DB_NAME)
CURSOR = CONNECTION.cursor()


logging.info('The current line: %s', CURRENT_LINE)
# Parse the CSV file
CSV_FILE = open(CSV_PATH, 'rU')
reader = csv.reader(CSV_FILE)
CURRENT_LINE = reader.next()
CURRENT_LINE = reader.next()

new_line_filtered = (line.replace('\n', ' ') for line in CSV_FILE)
tab_filtered = (line.replace('\t', ' ') for line in new_line_filtered)

for row in csv.reader(tab_filtered):
    print row

print CURRENT_LINE

print CURRENT_LINE[6]
date = datetime.strptime(CURRENT_LINE[6], '%B  %d, %Y')
print date.date()



insert_statement = ("INSERT INTO available_assets"
                    "(name, "
                    "model, "
                    "asset_id, "
                    "description, "
                    "created_by, "
                    "purchased_on, "
                    "price_$, "
                    "`group`, "
                    "sub_group, "
                    "vendor, "
                    "location, "
                    "allocated_to)"
                    "VALUES"
                    "(%(name)s, "
                    "%(model)s, "
                    "%(asset_id)s, "
                    "%(description)s, "
                    "%(created_by)s, "
                    "%(purchased_on)s, "
                    "%(price_$)s, "
                    "%(group)s, "
                    "%(sub_group)s, "
                    "%(vendor)s, "
                    "%(location)s, "
                    "%(allocated_to)s)")

insert_values = {'name': CURRENT_LINE[1],
                 'model': CURRENT_LINE[2],
                 'asset_id': CURRENT_LINE[3],
                 'description': CURRENT_LINE[4],
                 'created_by': CURRENT_LINE[5],
                 'purchased_on': date.date(),
                 'price_$': CURRENT_LINE[7],
                 'group': CURRENT_LINE[8],
                 'sub_group': CURRENT_LINE[9],
                 'vendor': CURRENT_LINE[10],
                 'location': CURRENT_LINE[11],
                 'allocated_to': CURRENT_LINE[12]}

print insert_values

CURSOR.execute(insert_statement, insert_values)
CONNECTION.commit()
CURSOR.close()
CONNECTION.close()