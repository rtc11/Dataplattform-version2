import boto3
import os
import json
import time
from bs4 import BeautifulSoup
import requests


def handler(event, context):
    poll()

    return {
        'statusCode': 200,
        'body': 'Success'
    }


def poll():
    data = {}

    

    path = os.getenv("ACCESS_PATH")
    s3 = boto3.resource('s3')
    s3_object = s3.Object(os.getenv('DATALAKE'), path +
                          str(int(time.time())) + ".json")
    s3_object.put(Body=(bytes(json.dumps(data).encode('UTF-8'))))
    return True


if __name__ == "__main__":
    poll()