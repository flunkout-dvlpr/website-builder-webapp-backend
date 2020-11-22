import datetime
import psycopg2

def connectToPostgress(databaseName):
  connection = psycopg2.connect(host = 'clean-code-llc.cogxlpoqzgkf.us-east-2.rds.amazonaws.com', 
                                port = 5432, 
                                dbname = databaseName, 
                                user = 'postgres', 
                                password = 'postgres')
  cursor = connection.cursor()
  return cursor

def datetime_handler(value):
  if isinstance(value, (datetime.datetime, datetime.date)):
      return value.isoformat()
  raise TypeError("Unknown type")
