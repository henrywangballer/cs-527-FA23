from __future__ import print_function

import json
import uuid
import decimal
import os
import boto3


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# Get the service resource.
LOCALSTACK_ENDPOINT = 'http://localhost.localstack.cloud:4566'
AWS_REGION = "us-east-1"
# Get the service resource.
dynamodb = boto3.resource("dynamodb", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']


def lambda_handler(event, context):
    print(f'===============inside producer lambda')
    table = dynamodb.Table(TABLE_NAME)
    # put item in table
    for i in range(20):
        print(f'==============put item')
        response = table.put_item(
            Item={
                'id': str(i)
            }
        )

        print("PutItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))

    return {
        'statusCode': 200,
    }