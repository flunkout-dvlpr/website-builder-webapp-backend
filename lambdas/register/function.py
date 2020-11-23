import json
from cleancode import *

def handler(event, context):
  body = json.loads(event['body'])
  name = body['name']
  address_1 = body['address_1']
  address_2 = body['address_2']
  phone = body['phone']
  email = body['email']
  zip_code = body['zip_code']
  city = body['city']
  state = body['state']
  db_name = body['db_name']

  try:
    ################# Use switch case to match db_name with table #################
    if (db_name == 'auto_shop_crm'):
      table_name = 'autoshop'
    ###############################################################################
    cursor = connectToPostgress(db_name)
    cursor.execute("""
      INSERT INTO
      autoshop (name, address_1, address_2, phone, email, zip_code, city, state)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
      RETURNING *;
    """, (name, address_1, address_2, phone, email, zip_code, city, state))
    columns = [column[0] for column in cursor.description]
    response = cursor.fetchone()
    record = dict(zip(columns, response))
    cursor.execute("COMMIT;")
  except:
    return {
        "statusCode": 200,
        "headers": {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps( {
          "type": "error",
          "message": "Registration Failed"
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
        "message": "Successfully Registered!",
        "payload": record
        }, default=datetime_handler)
    }

