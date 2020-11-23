import boto3
import json
from cleancode import * 

def handler(event, context):
  s3 = boto3.client('s3')
  body = json.loads(event['body'])
  template = body['template']
  businessId = body['id']
  sectionId = body['section']
  fileName = body['fileName']
  s3_bucket = "website-builder-webapp-data"

  s3_filename = '{}/{}/{}/{}'.format(template, businessId, sectionId, fileName)
  try:
    s3 = boto3.client('s3')
    link = s3.generate_presigned_url('put_object', Params = {'Bucket': s3_bucket, 'Key': s3_filename}, ExpiresIn = 6000, HttpMethod="PUT")
  except:
    return {
      'statusCode': 200,
      'headers': {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      "body": json.dumps( {
        "message": "Failed uploading file",
        "type": "error"
      }, default=datetime_handler)
    }

  return {
    'statusCode': 200,
    'headers': {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*"
    },
    "body": json.dumps( {
      "message": "File uploaded successfully",
      "type": "success",
      "payload": link
    }, default=datetime_handler)
  }