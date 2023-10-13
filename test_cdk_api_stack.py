import aws_cdk as cdk
from aws_cdk.assertions import Template

from cdk.api_cors_lambda_stack import ApiCorsLambdaStack

def test_cdk_api_stack():
    app = cdk.App()

    api_stack = ApiCorsLambdaStack(app, "ApiCorsLambdaStack")

    template = Template.from_stack(api_stack)

    # template.resource_count_is("AWS::IAM::Role", 1)
    template.has_resource("AWS::IAM::Role", {
        "Properties": {"RoleName": "LambdaRole"}
    })

    template.resource_count_is("AWS::ApiGateway::RestApi", 1)
    template.has_resource("AWS::ApiGateway::RestApi", {
        "Properties": {"Name": "ApiGatewayWithCors"}
    })

    template.resource_count_is("AWS::ApiGateway::Method", 4)


    template.has_resource("AWS::ApiGateway::Method", {
        "Properties": {"HttpMethod": "OPTIONS"}
    })
    template.has_resource("AWS::ApiGateway::Method", {
        "Properties": {"HttpMethod": "GET"}
    })

    template.resource_count_is("AWS::Lambda::Function", 2)
    template.has_resource("AWS::Lambda::Function", {
        "Properties": {"FunctionName": "ApiCorsLambda"}
    })
    template.has_resource("AWS::Lambda::Function", {
        "Properties": {"FunctionName": "QueryParamsLambda"}
    })


    # template.has_resource("AWS::S3::Bucket", {
    #     "Properties": {"BucketName": "mybucket2"}
    # })


