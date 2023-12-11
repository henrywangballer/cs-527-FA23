import boto3
import pytest
import os
import aws_cdk as core
import json
import requests

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
def apigw_client():
    return boto3.client("apigateway", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)


def test_bad_api(apigw_client):
    apis = apigw_client.get_rest_apis()
    api_name = apis["items"][0].get('name')
    apigw_id = apis["items"][0]['id']
    stage = 'prod'
    path = 'example'

    base_url = f"http://{apigw_id}.execute-api.localhost.localstack.cloud:4566/{stage}/{path}"

    response = requests.get(f"{base_url}")
    d = json.loads(response.text)

    assert response.status_code == 200
    assert d.get('errorType') == 'Runtime.HandlerNotFound'



def test_api_example1(apigw_client):
    apis = apigw_client.get_rest_apis()
    api_name = apis["items"][0].get('name')
    apigw_id = apis["items"][0]['id']
    stage = 'prod'
    path = 'example1'
    message = 'Hello from CS527!'
    query_params = f'message={message}'


    base_url = f"http://{apigw_id}.execute-api.localhost.localstack.cloud:4566/{stage}/{path}"

    response = requests.get(f"{base_url}?{query_params}")
    d = json.loads(response.text)

    assert response.status_code == 200


    expected_response_text = f'Message: {message}'
    assert expected_response_text == json.loads(response.text)