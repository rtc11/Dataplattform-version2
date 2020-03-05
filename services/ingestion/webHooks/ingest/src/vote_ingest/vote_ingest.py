import json
import boto3
import time

def handler(event, context):
    print('## VOTE_EVENT')
    print(event)
    
    data_type = event["pathParameters"]["type"]
    data = event["body"]

    if data_type not in types: return False
    
    path = '{type}/{time}.json'.format(type=data_type, time = int(time.time()))
    
    s3 = boto3.resource('s3')
    s3_object = s3.Object('dataplattform-eventbox-bucket', path)
    s3_object.put(Body=(bytes(json.dumps(data).encode('UTF-8'))))

    return {
        'statusCode': 200,
        'body': json.dumps({
            "message": "success!",
            "data_type": data_type,
            "data": data
        })
    }

types = ['VoteType', 'CommentType']