import boto3
import pytest
import os
import aws_cdk as core
import json
import time

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

@pytest.fixture
def transcribe_client():
    return boto3.client("transcribe", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)


def test_transcribe_lambda(lambda_client):
    response = lambda_client.invoke(
        FunctionName='TranscribeLambda',
        InvocationType='RequestResponse',
    )
    print(response)
    assert response['StatusCode'] == 200

    response_payload = response.get('Payload').read().decode()
    # print(response_payload)
    parsed_response = json.loads(response_payload)
    print(parsed_response.get('body'))

    assert parsed_response.get('body')[1:-1].startswith('thank you for calling')



def test_s3(s3_client):
    bucket_name = 'inputtranscribebucket'
    response = s3_client.list_objects(Bucket='inputtranscribebucket', Prefix='example-call.wav')

    print(response)
    assert response.get('Contents') != None

