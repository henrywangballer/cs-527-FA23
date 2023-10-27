import aws_cdk as cdk
from aws_cdk.assertions import Template
from cdk.lambda_layer_stack import LambdaLayerStack

def test_cdk_lambda_layer_stack():
    app = cdk.App()

    api_stack = LambdaLayerStack(app, "LambdaLayerStack")
    template = Template.from_stack(api_stack)

    # template.resource_count_is("AWS::IAM::Role", 1)
    template.has_resource("AWS::IAM::Role", {
        "Properties": {"RoleName": "LambdaLayerRole"}
    })

    template.resource_count_is("AWS::Lambda::Function", 1)
    template.has_resource("AWS::Lambda::Function", {
        "Properties": {"FunctionName": "layer_function",
                       "Runtime": "python3.8"}
    })


    template.resource_count_is("AWS::Lambda::LayerVersion", 1)
    template.has_resource("AWS::Lambda::LayerVersion", {
        "Properties": {"LayerName": "helper_layer", "CompatibleRuntimes": ["python3.8", "python3.9", "python3.10"]}
    })





