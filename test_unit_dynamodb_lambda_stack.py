import boto3
import pytest
import os
import aws_cdk as core
import json

# Replace these with your LocalStack service endpoint and region
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"


@pytest.fixture
def s3_client():
    return boto3.client("s3", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)


@pytest.fixture
def db_client():
    return boto3.client("dynamodb", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def lambda_client():
    return boto3.client("lambda", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)


# def test_insert_dynamodb(db_client):
#     table = 'demo_table'
#
#     items = [
#         {"id": {'S': 'cs527'}},
#         {"id": {'S': 'cs511'}},
#         {'id': {'S': 'cs411'}},
#         {'id': {'S': 'cs427'}}
#     ]
#
#     for item in items:
#         db_client.put_item(
#             TableName=table,
#             Item=item
#         )
#     response = db_client.scan(TableName=table)
#     response_items = response.get('Items', [])
#     # assert len(response_items) == len(items)

def test_producer_lambda(lambda_client):
    response = lambda_client.invoke(
        FunctionName='producer_lambda_function',
        InvocationType='RequestResponse',
    )

    assert response['StatusCode'] == 200


def test_consumer_lambda(lambda_client):
    response = lambda_client.invoke(
        FunctionName='consumer_lambda_function',
        InvocationType='RequestResponse',
    )
    response_payload = response.get('Payload').read().decode()
    # print(response_payload)
    parsed_response = json.loads(response_payload)
    # print(parsed_response)

    body = json.loads(parsed_response.get('body'))

    values = [int(item['id']) for item in body]
    values.sort()
    # print(values)

    assert all(num in values for num in range(20))
