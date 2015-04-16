#!/usr/bin/evn python2

__author__ = 'apinchuk'

import sys
import logging
import MySQLdb as db
import mysql.connector as connector
import config
import csv
from datetime import datetime

#This is a file that is to be converted into a database
CSV_PATH = sys.argv[1]
CSV_FILE = None
CURRENT_LINE = None
CURSOR = None
DB_NAME = 'Assets'

#Show ALL the debug info by default
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



CURRENT_LINE = CSV_FILE.readline()
logging.info('The current line: %s', CURRENT_LINE)
#Parse the CSV file
f = open(CSV_PATH, 'rt')
reader = csv.reader(f)
CURRENT_LINE = reader.next()
CURRENT_LINE = reader.next()
print CURRENT_LINE

print CURRENT_LINE[6]
date = datetime.strptime(CURRENT_LINE[6], '%B  %d, %Y').date()
print date


date = {'date': datetime.strptime(CURRENT_LINE[6], '%B  %d, %Y').date()}

print date['date']


def string_to_date(string):
    """Turn string object into date"""
    date_to_return = datetime.strptime(string, '%B  %d, %Y').date()
    return date_to_return