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
def kinesis_client():
    return boto3.client("kinesis", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)


@pytest.fixture
def firehose_client():
    return boto3.client("firehose", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)


def test_kinesis(kinesis_client, s3_client, firehose_client):
    kinesis_stream_name = 'KinesisStream'
    s3_bucket_name = 'kinesisbucket'
    firehose_stream_name = 'firehose-stream'


    response = kinesis_client.put_record(
        StreamName=kinesis_stream_name,
        Data=b'bytes',
        PartitionKey='example_partition_key'
    )

    print("Record added to Kinesis stream:", response)

    time.sleep(60)
    response = firehose_client.describe_delivery_stream(DeliveryStreamName=firehose_stream_name)

    print("Firehose Delivery Stream Status:", response['DeliveryStreamDescription']['DeliveryStreamStatus'])

    # firehose_client.put_record(
    #     DeliveryStreamName=firehose_stream_name,
    #     Record={
    #         'Data':b'bytes'
    #     }
    # )

    # List objects in the S3 bucket
    response = s3_client.list_objects(Bucket=s3_bucket_name)

    print("Objects in S3 Bucket:", response.get('Contents', []))