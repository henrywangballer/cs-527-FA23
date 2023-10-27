import boto3
import pytest
import os
import aws_cdk as core
from cdk.sqs_sns_stack import S3SnsSqsLambdaChainStack

# Replace these with your LocalStack service endpoint and region
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"


@pytest.fixture
def s3_client():
    return boto3.client("s3", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def sns_client():
    return boto3.client("sns", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def sqs_client():
    return boto3.client("sqs", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def lambda_client():
    return boto3.client("lambda", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)


@pytest.fixture
def app():
    # Create a CDK app and stack
    cdk_output_dir = "cdk.out"

    app = core.App()
    S3SnsSqsLambdaChainStack(app, "SnsSqsStack")

    # Deploy the CDK stack
    app.synth()
    os.system(f"cdklocal deploy -a {cdk_output_dir} S3SnsSqsLambdaChainStack")
    yield app


def test_s3_buckets(app, s3_client):

    buckets = s3_client.list_buckets()
    print(buckets)

    bucket_names = [bucket["Name"] for bucket in buckets["Buckets"]]

    expected_bucket_name = "sns-bucket"

    assert expected_bucket_name in bucket_names, f"Expected {expected_bucket_name} buckets, but found {bucket_names}."

def test_sns(sns_client):
    # subs = sns_client.list_subscriptions()
    # print(subs)

    topics = sns_client.list_topics()
    print(topics)
    expected_topic_name = 'sns_upload_topic'

    topic_names = []
    for topic in topics.get('Topics'):
        topic_arn = topic['TopicArn']
        topic_names.append(topic_arn.split(':')[-1])

    assert expected_topic_name in topic_names

def test_sqs(sqs_client):
    queues = sqs_client.list_queues()
    print(queues)

    queue_names = []
    for queue in queues.get("QueueUrls"):
        queue_names.append(queue.split('/')[-1])

    expected_queue_names = ['dead_letter_queue', 'upload_queue']
    for q in expected_queue_names:
        assert q in queue_names

def test_sqs_attributes(sqs_client):
    queues = sqs_client.list_queues()
    print(queues)

    queue_urls = []
    for queue in queues.get("QueueUrls"):
        queue_urls.append(queue)

    for url in queue_urls:
        response = sqs_client.get_queue_attributes(
            QueueUrl=url,
            AttributeNames=['All']
        )
        print(response)
        if url.split('/')[-1] == 'dead_letter_queue':
            expected_message_retention_period = '604800'
            assert response.get('Attributes').get('MessageRetentionPeriod') == expected_message_retention_period
        if url.split('/')[-1] == 'upload_queue':
            expected_visibilityTimeout = str(30*6)
            assert response.get('Attributes').get('VisibilityTimeout') == expected_visibilityTimeout


def test_lambda(lambda_client):
    functions = lambda_client.list_functions()
    print(functions)

    func_items = [{'name': d['FunctionName'], 'runtime':  d['Runtime']} for d in functions['Functions']]
    expected_funcs = [{'name': 'sqs_sns_lambda', 'runtime': 'python3.10'}]
    assert all(func in func_items for func in expected_funcs)
