import os
import urllib.request
import xmltodict
import json
import boto3
import time



def handler(event, context):
    poll()

    return {
        'statusCode': 200,
        'body': ''
    }

def poll():
    location = os.getenv("DATAPLATTFORM_YR_LOCATION")

    data = get_yr_data(location)
    put_in_datalake(data)

def get_yr_data(location):
    # I dette eksempelet puttes alle værevarsler inn i S3. Dette er et litt forenklet eksempel der nesten all data
    # legges rå inn i S3. Det kan være ønskelig å filtrere i litt større grad.
    # F.eks å begrense værdata som lagres til bare de neste 24 timene. Det kan være aktuelt å bruke en DynamoDB table
    # for å holde styr på "last_inserted_doc" slik som i den "gamle" arkitekturen

    url = f"https://www.yr.no/place/{location}/varsel_time_for_time.xml"

    response = send_request(url)
    data = xmltodict.parse(response)

    filtered_data = json.dumps(filter_response(data))
    return filtered_data

def send_request(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    return response.read().decode()


def filter_response(data):
    filtered_data = {'yrdata': {}}
    filtered_data['yrdata']['location'] = data["weatherdata"]["location"]['name']
    filtered_data['yrdata']['forecasts'] = data["weatherdata"]["forecast"]["tabular"]["time"]
    return filtered_data

def put_in_datalake(data):
    s3 = boto3.resource('s3')
    s3_object = s3.Object(os.getenv('DATALAKE'), os.getenv('DATALAKE_PATH') + str(int(time.time())) + '.json')
    s3_object.put(Body=data)

