import aws_cdk as cdk
from aws_cdk.assertions import Template
from cdk.dynamodb_lambda_stack import DynamodbLambdaStack

def test_cdk_dynamodb_lambda_stack():
    app = cdk.App()

    api_stack = DynamodbLambdaStack(app, "DbStack")
    template = Template.from_stack(api_stack)

    # template.resource_count_is("AWS::IAM::Role", 1)
    template.has_resource("AWS::IAM::Role", {
        "Properties": {"RoleName": "LambdaRole"}
    })

    template.resource_count_is("AWS::DynamoDB::Table", 1)
    template.has_resource("AWS::DynamoDB::Table", {
        "Properties": {"TableName": "demo_table",
                       "AttributeDefinitions": [
                           {
                               "AttributeName": "id",
                               "AttributeType": "S"
                           }]
                       }
    })

    template.resource_count_is("AWS::Lambda::Function", 2)
    template.has_resource("AWS::Lambda::Function", {
        "Properties": {"FunctionName": "producer_lambda_function",
                       "Runtime": "python3.10"}
    })
    template.has_resource("AWS::Lambda::Function", {
        "Properties": {"FunctionName": "consumer_lambda_function",
                       "Runtime": "python3.10"}
    })

    template.resource_count_is("AWS::Events::Rule", 1)
    template.has_resource("AWS::Events::Rule", {
        "Properties": {"Name": "one_minute_rule"}
    })
    template.has_resource("AWS::Events::Rule", {
        "Properties": {"Name": "one_minute_rule"}
    })




