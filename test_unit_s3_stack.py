import boto3
import pytest
import os
import aws_cdk as core


# Replace these with your LocalStack service endpoint and region
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"


@pytest.fixture
def s3_client():
    return boto3.client("s3", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

def test_S3(s3_client):
    bucket_name = 'mybucket'
    s3_client.put_object(Body='mybucket test 1', Bucket=bucket_name, Key='item1')

    expected_key = 'item1'
    response = s3_client.list_objects(Bucket=bucket_name, Prefix='expected_key')


    print(response)
    assert response.get('Contents') != []

def test_s3(s3_client):
    bucket_name='mybucket1'
    s3_client.upload_file('./txt_files/text1.txt', bucket_name, 'text1.txt')

    assert s3_client.head_object(Bucket=bucket_name, Key='text1.txt')