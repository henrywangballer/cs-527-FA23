import pytest
import aws_cdk as core
from cdk.project_stack import ProjectStack # Import your CDK stack
from moto import mock_s3
import boto3

@pytest.fixture
def app():
    app = core.App()
    ProjectStack(app, "MyStack")
    return app

@mock_s3
def test_my_cdk_app_with_moto_s3(app):

    with mock_s3():
        s3_client = boto3.client("s3", region_name="us-east-1")

        # List S3 buckets
        buckets = s3_client.list_buckets()
        print(buckets)
        assert len(buckets["Buckets"]) == 0  # No buckets should exist in the mock

        s3_client.create_bucket(Bucket="my-test-bucket")

        buckets = s3_client.list_buckets()
        assert len(buckets["Buckets"]) == 1
