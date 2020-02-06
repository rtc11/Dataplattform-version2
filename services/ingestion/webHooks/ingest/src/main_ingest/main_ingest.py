import json
import boto3
import os

s3 = boto3.client('s3')
bucket_name = os.environ['DATA_LAKE']

def handler(event, context):
    data_type = event["pathParameters"]["type"]
    data = event["body"]

    s3.put_object(
        Bucket=bucket_name,
        Key=data_type+'/this_file',
        Body=data,
        Tagging="level:public"

    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            "message": "success!",
            "data_type": data_type,
            "data": data
        })
    }

#TO DO!
# hvordan organisere insetting?
# skal en lambda gjøre alt?
# skal vi bruke serverside encryption?
# hvordan skal vi tagge data?
# hvordan skal data lagres? mappestruktur, objectnavn, pakkes?
# add MFA deleting i s3?
