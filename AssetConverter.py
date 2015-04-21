#!/usr/bin/evn python2

__author__ = 'apinchuk'

import sys
import logging
import mysql.connector as connector
from datetime import datetime
import config
import csv


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

# Login into MySQL check if the database exists, and create it if it does not.
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

# Connect to the actual database (existed or created)
CONNECTION = connector.connect(user=config.database['user'], database=DB_NAME)
CURSOR = CONNECTION.cursor()


logging.info('The current line: %s', CURRENT_LINE)
# Parse the CSV file
CSV_FILE = open(CSV_PATH, 'rU')
reader = csv.reader(CSV_FILE)
next(reader) # Skip two first header lines
next(reader)


# Remove all the newlines and tabs from the file
new_line_filtered = (line.replace('\n', ' ') for line in CSV_FILE)
tab_filtered = (line.replace('\t', ' ') for line in new_line_filtered)

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
                    "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")




for CURRENT_LINE in csv.reader(tab_filtered):
    # Convert the date from string into appropriate MySQL format
    CURRENT_LINE[6] = datetime.strptime(CURRENT_LINE[6], '%B  %d, %Y')
    insert_values = (CURRENT_LINE[1], CURRENT_LINE[2], CURRENT_LINE[3], CURRENT_LINE[4], CURRENT_LINE[5],
                     CURRENT_LINE[6], CURRENT_LINE[7], CURRENT_LINE[8], CURRENT_LINE[9], CURRENT_LINE[10],
                     CURRENT_LINE[11], CURRENT_LINE[12])
    print insert_values
    CURSOR.execute(insert_statement, insert_values)

CONNECTION.commit()
CURSOR.close()
CONNECTION.close()