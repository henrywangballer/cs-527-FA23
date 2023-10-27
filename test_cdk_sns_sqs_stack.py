import aws_cdk as cdk
from aws_cdk.assertions import Template

from cdk.sqs_sns_stack import S3SnsSqsLambdaChainStack

def test_cdk_sns_sqs_stack():
    app = cdk.App()

    sns_sqs_stack = S3SnsSqsLambdaChainStack(app, "MyS3Stack")

    template = Template.from_stack(sns_sqs_stack)

    template.resource_count_is("AWS::S3::Bucket", 1)
    template.has_resource("AWS::S3::Bucket", {
        "Properties": {"BucketName": "sns-bucket"}
    })

    template.has_resource("AWS::SQS::Queue", {
        "Properties": {
                "MessageRetentionPeriod": 604800,
                "QueueName": "dead_letter_queue"
            }
    })

    template.has_resource("AWS::SQS::Queue", {
        "Properties": {
            "VisibilityTimeout": 180,
            "QueueName": "upload_queue"
        }
    })

    template.has_resource("AWS::Lambda::Function", {
        "Properties": {"FunctionName": "sqs_sns_lambda",
                       "Runtime": "python3.10"}
    })

    template.has_resource("AWS::SNS::Topic", {
        "Properties": {
            "TopicName": "sns_upload_topic"
        }
    })



