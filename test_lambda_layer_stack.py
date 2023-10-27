import boto3
import pytest
import os
import aws_cdk as core
from cdk.lambda_layer_stack import LambdaLayerStack

# Replace these with your LocalStack service endpoint and region
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"



@pytest.fixture
def lambda_client():
    return boto3.client("lambda", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)


@pytest.fixture
def app():

    cdk_output_dir = "cdk.out"
    app = core.App()
    LambdaLayerStack(app, "LambdaLayerStack")

    # Deploy the CDK stack
    app.synth()
    os.system(f"cdklocal deploy -a {cdk_output_dir} LambdaLayerStack")
    yield app


def test_lambda_function(app, lambda_client):

    functions = lambda_client.list_functions()
    print(functions)

    func_items = [{'name': d['FunctionName'], 'runtime': d['Runtime']} for d in functions['Functions']]
    print(func_items)
    expected_funcs = [{'name': 'layer_function', 'runtime': 'python3.8'}]
    assert all(func in func_items for func in expected_funcs)

def test_lambda_layer_stack(lambda_client):
    layers = lambda_client.list_layers()
    print(layers)
    expected_layers = [{'LayerName': 'helper_layer', 'CompatibleRuntimes': ['python3.8', 'python3.9', 'python3.10']}]
    layer_items = [{'LayerName': l['LayerName'], 'CompatibleRuntimes': l['LatestMatchingVersion']['CompatibleRuntimes']} for l in layers['Layers']]

    assert all(layer in layer_items for layer in expected_layers)