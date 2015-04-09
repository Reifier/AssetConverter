#!/usr/bin/evn python2

__author__ = 'apinchuk'

import sys
import logging
import MySQLdb as db
import mysql.connector as connector
import config

#This is a file that is to be converted into a database
CSV_PATH = sys.argv[1]
CSV_FILE = None
CURRENT_LINE = None
CURSOR = None

#Show ALL the debug info by default
logging.basicConfig(level=logging.DEBUG)


logging.info('The file to process: %s', CSV_PATH)

CSV_FILE = open(CSV_PATH)
CURRENT_LINE = CSV_FILE.readline()
logging.info('The current line: %s', CURRENT_LINE)

logging.debug('The user to be logged in: %s', config.database['user'])


def get_user_cursor():
    """A function that creates a cursor with a certain user"""
    connection = connector.connect(**config.database)
    cursor = connection.cursor()
    logging.debug('The current DB user is: %s', connection.user)
    return cursor

CURSOR = get_user_cursor()
