import json
import psycopg2
from psycopg2 import sql
from cleancode import *

def handler(event, context):
  body = json.loads(event['body'])
  registration = body
  recordId = body['id']
  db_name = body['db_name']
  [registration.pop(key, None) for key in ['id', 'db_name', 'created_on', 'status', 'template']]
  
  try:
    ################# Use switch case to match db_name with table #################
    if (db_name == 'auto_shop_crm'):
      table_name = 'autoshop'
    ###############################################################################

    cursor = connectToPostgress(db_name)
    for column, value in registration.items():
      sql_query = sql.SQL("UPDATE {table} SET {field} = %s WHERE {pkey} = %s RETURNING *;").format(
        table=sql.Identifier(table_name),
        field=sql.Identifier(column),
        pkey=sql.Identifier('id'))
      cursor.execute(sql_query, (value, recordId,))
      columns = [column[0] for column in cursor.description]
      response = cursor.fetchone()
      responseInDict = dict(zip(columns, response))
    cursor.execute("COMMIT;")
  
  except:
    return {
        'statusCode': 200,
        'headers': {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps( {
          "type": "error",
          "message": "Failed updating registration",
        })
      }
  
  return {
      'statusCode': 200,
      'headers': {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      'body': json.dumps( {
        "type": "success",
        "message": "Successfully updated registration!",
        "payload":responseInDict
        }, default=datetime_handler)
    }