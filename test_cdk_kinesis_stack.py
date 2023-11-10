import aws_cdk as cdk
from aws_cdk.assertions import Template

from cdk.kinesis_stack import LambdaWithKinesisTrigger

def test_cdk_api_stack():
    app = cdk.App()

    api_stack = LambdaWithKinesisTrigger(app, "LambdaWithKinesisTrigger")

    template = Template.from_stack(api_stack)

    template.has_resource("AWS::Kinesis::Stream", {
        "Properties": {"Name": "KinesisStream",
                       "ShardCount": 1}
    })

    template.has_resource("AWS::Lambda::Function", {
        "Properties": {"FunctionName": "kinesisLambda",
                       "Handler":"index.main",
                       "Runtime": "python3.9"}
    })

    template.has_resource("AWS::Lambda::EventSourceMapping", {
        "Properties": {"BatchSize": 1,
                       "StartingPosition": "LATEST"}
    })



