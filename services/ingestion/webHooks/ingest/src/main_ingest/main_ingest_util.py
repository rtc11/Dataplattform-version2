import boto3
import os

class IngestUtil:
    __bucket = None

    @staticmethod
    @staticmethod
    def get_bucket():
        if IngestUtil.__bucket is None:
            IngestUtil.__bucket = boto3.client('s3')
            bucket_name = os.environ['DATA_LAKE']
        return IngestUtil.__bucket

    @staticmethod
    def insert_object(type, data=None, timestamp=None):
        if data is None:
            return