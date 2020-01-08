# coding: utf-8

import time
import sys
import os
import datetime
import sqlite3

#connection = sqlite3.co#! python3c
connection = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + "\\settings.db") #Windows
cursor = connection.cursor()

acttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#Request Gensetnumber
SQL_Command = """UPDATE timestampe SET updatetime = '{0}' WHERE id = '1'""".format(acttime)
cursor.execute(SQL_Command)
connection.commit()
SQL_Command = None # emtpy variable

connection.close()