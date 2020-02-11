import json
import boto3

def handler(event, context):
    for record in event['Records']:
        process_object(record['s3']['bucket']['name'], record['s3']['object']['key'])


def process_object(bucket_name, object_name):
    data = get_object(bucket_name, object_name)

    # for testing. fjernes
    print(data)

    # videre vil typ data bli filtrert, strukturert og lagt inn i en SQL database (bruk SQLAlchemy for dette)


def get_object(bucket_name, object_name):
    s3 = boto3.client('s3')

    obj = s3.get_object(
        Bucket=bucket_name,
        Key=object_name
    )

    return obj['Body'].read().decode('utf-8')


