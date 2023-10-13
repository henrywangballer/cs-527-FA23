import boto3
import pytest
import os
import aws_cdk as core
from cdk.dynamodb_lambda_stack import DynamodbLambdaStack

# Replace these with your LocalStack service endpoint and region
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"


@pytest.fixture
def db_client():
    # print('s3client1=1=1==1')
    return boto3.client("dynamodb", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def lambda_client():
    return boto3.client("lambda", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def events_client():
    return boto3.client("events", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def app():
    # Create a CDK app and stack
    cdk_output_dir = "cdk.out"
    # os.makedirs(cdk_output_dir, exist_ok=True)
    # os.environ["CDK_OUTDIR"] = ""
    app = core.App()
    DynamodbLambdaStack(app, "DbStack")

    # Deploy the CDK stack
    app.synth()
    # print('testapp======================')
    os.system(f"cdklocal deploy -a {cdk_output_dir} DynamodbLambdaStack")
    yield app


def test_count_s3_buckets(app, lambda_client):

    functions = lambda_client.list_functions()
    print(functions)

    func_items = [{'name': d['FunctionName'], 'runtime': d['Runtime']} for d in functions['Functions']]
    expected_funcs = [{'name': 'producer_lambda_function', 'runtime': 'python3.10'},
                      {'name': 'consumer_lambda_function', 'runtime': 'python3.10'}]
    assert all(func in func_items for func in expected_funcs)

def test_db_tables(db_client):
    tables = db_client.list_tables()
    print(tables)

    expected_table_name = 'demo_table'
    assert expected_table_name in tables.get('TableNames')

def test_event_rules(events_client):
    rules = events_client.list_rules()
    print(rules)

    expected_rule_name = 'one_minute_rule'
    assert expected_rule_name in [r['Name'] for r in rules['Rules']]