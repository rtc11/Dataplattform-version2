import boto3
import json
import os
import boto3
from botocore.client import Config
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, BigInteger, Integer, String, MetaData, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


"""
Example event: 
{
    "Records": [
        {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "awsRegion": "eu-central-1",
            "eventTime": "2020-02-27T14:32:16.245Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
                "principalId": "AWS:AIDAVC5W4ROCCG2YGJWRA"
            },
            "requestParameters": {
                "sourceIPAddress": "213.236.166.194"
            },
            "responseElements": {
                "x-amz-request-id": "6942494D6E20F1FA",
                "x-amz-id-2": "u7sLSXVmMYQbbu0n8s5pOHDcSow98qLiG5oot49htClIJhtHeyz7VETpWZxM8YTaauPLnYscCBhsrHX+JRm6ndQZld7oiRIS"
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "dev-GoogleEventProcessor-e591532d98f0a1b8c17e69f6303a1878",
                "bucket": {
                    "name": "dataplattform-eventbox-bucket",
                    "ownerIdentity": {
                        "principalId": "A2CG4HAW1G53A4"
                    },
                    "arn": "arn:aws:s3:::dataplattform-eventbox-bucket"
                },
                "object": {
                    "key": "GoogleCalendarEvents/testjsonfil.json",
                    "size": 276,
                    "eTag": "23882984642abf3a9950cd34bb659782",
                    "sequencer": "005E57D2F48281E33B"
                }
            }
        }
    ]
}
"""

def handler(event, context):
	# Fetch all data from s3 first to insert all data in one DB-Session
#	data = {}
#	for record in event['Records']:
#		data.update(record['s3']['bucket']['name'], get_data_from_s3(record['s3']['object']['key']))
	engine = get_engine()
	bucket_name = event['Records'][0]['s3']['bucket']['name']
	bucket_object = event['Records'][0]['s3']['object']['key']
	s3_data = get_data_from_s3(bucket_name, bucket_object)
	print(s3_data)
	return {
		"statusCode": 200,
		"body": s3_data
	}


def process_data(data):
###########################################TODO#####################################################
#	Fetch google events from db for the next 24 hours
#	Compare s3 data with db data
#	If event from s3 does not exist in db then insert into db
#	Else if event has same Id but different attributes insert again DO NOT DELETE PREVIOUS EVENT
#	Else do nothing
#	
#	Reference: https://github.com/knowit/Dataplattform/tree/master/services/structured_mysql/update
####################################################################################################
	print("Function can't be empty")


def get_data_from_s3(bucket, object):
	print("bucket")
	print(bucket)
	print("key")
	print(object)
	client = boto3.resource('s3')
	print("client")
	print(client)
	response = client.Object(
		bucket,
		object
	)
	print("response")
	print(response)
	return response.get()['Body'].read().decode('utf-8')


def get_engine():
#	VIL EGENTLIG HA DETTE, MEN MÅ ORDNE NOE MED VPC OG NOE GREIER ¯\_(ツ)_/¯
#	https://stackoverflow.com/questions/52134100/parameter-store-request-timing-out-inside-of-aws-lambda -- Tror dette er problemet
#
#	stage = os.getenv('STAGE')
#	parameter_path = "/{}/rds/postgres/".format(stage)
#	client = boto3.client('ssm')
#	response_username = client.get_parameter(
#		Name=parameter_path + "username",
#		WithDecryption=False)
#	response_password = client.get_parameter(
#		Name=parameter_path + "password", 
#		WithDecryption=True)
#
#	username = response_username['Parameter']['Value']
#	password = response_password['Parameter']['Value']

	username = os.getenv('DATABASE_USERNAME')
	password = os.getenv('DATABASE_PASSWORD')
	host = os.getenv('DATABASE_ENDPOINT_ADDRESS')
	port = os.getenv('DATABASE_ENDPOINT_PORT')
	engine = create_engine('postgresql://{}:{}@{}:{}/Dataplattform'.format(username, password, host, port), echo=False)
	return engine


def create_table(engine):
	Events.__table__.create(engine)


def drop_table(engine):
	Events.__table__.drop(engine)


def insert_data(session, id, event_summary, creator, start, end, event_code, active=False):
	
	event = Events(
		id=id, 
		event_summary=event_summary, 
		creator=creator, 
		start=start, 
		end=end, 
		event_code=event_code, 
		active=active)
	
	session.add(event)
	session.commit()


def get_all_data(session):
	# Returns list of Events for all objects in table
	return session.query(Events).all()


Base = declarative_base()

class Events(Base):
	__tablename__ = 'events'

	id = Column(String(100), primary_key = True)
	created_timestamp = Column(BigInteger, primary_key = True)
	event_summary = Column(String(255))
	creator = Column(String(255))
	start_timestamp = Column(BigInteger)
	end_timestamp = Column(BigInteger)
	



if __name__== "__main__":
	handler(None, None)