import boto3
import pytest
import os
import aws_cdk as core
import subprocess
from cdk.kinesis_stack import LambdaWithKinesisTrigger

# Replace these with your LocalStack service endpoint and region
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"


@pytest.fixture
def kinesis_client():
    return boto3.client("kinesis", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def lambda_client():
    return boto3.client("lambda", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def app():
    cdk_output_dir = "cdk.out"

    app = core.App()
    LambdaWithKinesisTrigger(app, "LambdaWithKinesisTrigger")

    app.synth()
    subprocess.run(f"cdklocal deploy -a {cdk_output_dir} LambdaWithKinesisTrigger", shell=True)
    yield app


def test_lambda(app, lambda_client):
    functions = lambda_client.list_functions()
    print(functions)

    func_items = [{'name': d['FunctionName'], 'runtime':  d['Runtime']} for d in functions['Functions']]
    expected_funcs = [{'name': 'kinesisLambda', 'runtime': 'python3.9'}]
    assert all(func in func_items for func in expected_funcs)


def test_kinesis(kinesis_client):
    streams = kinesis_client.list_streams()
    print(streams)

    expected_stream_name = 'KinesisStream'
    assert expected_stream_name in streams.get('StreamNames')


