import MySQLdb
import peewee
from peewee import *

db = MySQLdb.connect(host="***REMOVED***",    # your host, usually localhost
                     user="***REMOVED***",        
                     passwd="***REMOVED***",
                     db="socialnetworkingdb")        

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

print cur

# Use all the SQL you like
cur.execute("CREATE TABLE CUSTOMERS(ID INT NOT NULL, NAME VARCHAR (20) NOT NULL, PRIMARY KEY (ID));")

# print all the first cell of all the rows
# for row in cur.fetchall():
#     print row[0]

db.close()
