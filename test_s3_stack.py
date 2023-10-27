import boto3
import pytest
import os
import aws_cdk as core
from cdk.s3_stack import S3Stack

# Replace these with your LocalStack service endpoint and region
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"


@pytest.fixture
def s3_client():
    return boto3.client("s3", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def app():
    # Create a CDK app and stack
    cdk_output_dir = "cdk.out"

    app = core.App()
    S3Stack(app, "MyS3Stack")

    # Deploy the CDK stack
    app.synth()
    os.system(f"cdklocal deploy -a {cdk_output_dir} S3Stack")
    yield app


def test_count_s3_buckets(app, s3_client):

    buckets = s3_client.list_buckets()
    print(buckets)

    bucket_count = len(buckets["Buckets"])
    bucket_names = [bucket["Name"] for bucket in buckets["Buckets"]]

    expected_bucket_count = 1  # Modify as needed
    expected_bucket_name = "mybucket"

    # assert bucket_count == expected_bucket_count, f"Expected {expected_bucket_count} buckets, but found {bucket_count}."
    assert expected_bucket_name in bucket_names, f"Expected {expected_bucket_name} buckets, but found {bucket_names}."

