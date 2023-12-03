from __future__ import print_function

import json
import decimal
import os
import boto3
from botocore.exceptions import ClientError


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


LOCALSTACK_ENDPOINT = 'http://localhost.localstack.cloud:4566'
AWS_REGION = "us-east-1"
# Get the service resource.
dynamodb = boto3.resource("dynamodb", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']


def lambda_handler(event, context):
    # print(f'{TABLE_NAME}==============')
    table = dynamodb.Table(TABLE_NAME)

    payload = []
    # Scan items in table
    try:
        response = table.scan()
        payload = response['Items']
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        # print item of the table - see CloudWatch logs
        for i in response['Items']:
            print(json.dumps(i, cls=DecimalEncoder))

    return {
        'statusCode': 200,
        'body': json.dumps(payload)
    }