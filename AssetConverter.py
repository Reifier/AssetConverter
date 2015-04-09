#!/usr/bin/evn python2

__author__ = 'apinchuk'

import sys
import logging
import MySQLdb as db
import mysql.connector as connector

#This is a file that is to be converted into a database
CSV_PATH = sys.argv[1]
CSV_FILE = None
CURRENT_LINE = None

#Show ALL the debug info by default
logging.basicConfig(level=logging.DEBUG)


logging.info('The file to process: %s', CSV_PATH)

CSV_FILE = open(CSV_PATH)
CURRENT_LINE = CSV_FILE.readline()
logging.info('The current line: %s', CURRENT_LINE)


def connect_to_db(database):
    """A function that connects to a specified database"""

