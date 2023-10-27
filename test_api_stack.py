import boto3
import pytest
import os
import aws_cdk as core
import subprocess
from cdk.api_cors_lambda_stack import ApiCorsLambdaStack

# Replace these with your LocalStack service endpoint and region
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"


@pytest.fixture
def apigw_client():
    return boto3.client("apigateway", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def lambda_client():
    return boto3.client("lambda", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def app():
    # Create a CDK app and stack
    # target_directory = '..\..\..\cdk-localstack'
    # os.chdir(target_directory)
    #
    # print(os.getcwd())
    # cdk_output_dir = "..\..\cdk.out"

    cdk_output_dir = "cdk.out"
    # os.makedirs(cdk_output_dir, exist_ok=True)
    # os.environ["CDK_OUTDIR"] = "cdk_output_dir"
    app = core.App()
    ApiCorsLambdaStack(app, "ApiCorsLambdaStack")

    # Deploy the CDK stack
    app.synth()
    # print('testapp======================')
    # os.system(f"cdklocal deploy -a {cdk_output_dir}")
    subprocess.run(f"cdklocal deploy -a {cdk_output_dir} ApiCorsLambdaStack", shell=True)
    yield app


def test_apigw(app, apigw_client, lambda_client):

    apis = apigw_client.get_rest_apis()
    print(apis)
    api_count = len(apis["items"])
    api_name = apis["items"][0].get('name')
    apigw_id = apis["items"][0]['id']

    expected_api_count = 1
    assert expected_api_count == api_count

    expected_api_name = 'ApiGatewayWithCors'
    assert expected_api_name == api_name

    validators = apigw_client.get_request_validators(
        restApiId=apigw_id
    )
    validators_count = len(validators["items"])

    expected_validators_count = 1
    assert expected_validators_count == validators_count


    functions = lambda_client.list_functions()
    print(functions)
    # functions_count = len(functions['Functions'])
    # expected_func_count = 2
    # assert expected_func_count == functions_count

    func_items = [{'name': d['FunctionName'], 'runtime':  d['Runtime']} for d in functions['Functions']]
    expected_funcs = [{'name': 'QueryParamsLambda', 'runtime': 'python3.9'}, {'name': 'ApiCorsLambda', 'runtime': 'python3.9'}]
    assert all(func in func_items for func in expected_funcs)





