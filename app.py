#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.api_cors_lambda_stack import ApiCorsLambdaStack
from cdk.s3_stack import S3Stack
from cdk.dynamodb_lambda_stack import DynamodbLambdaStack
from cdk.lambda_layer_stack import LambdaLayerStack
from cdk.rekognition_lambda_s3_trigger_stack import RekognitionLambdaS3TriggerStack
from cdk.sqs_sns_stack import S3SnsSqsLambdaChainStack
from cdk.ec2_stack import EC2InstanceStack
from cdk.kinesis_stack import LambdaWithKinesisTrigger
from cdk.kinesis_s3_stack import KinesisS3

app = cdk.App()

ApiCorsLambdaStack(app, "ApiCorsLambdaStack",)
S3Stack(app, "S3Stack")
DynamodbLambdaStack(app, 'DynamodbLambdaStack')
LambdaLayerStack(app, 'LambdaLayerStack')
# RekognitionLambdaS3TriggerStack(app, 'RekognitionLambdaS3TriggerStack')
S3SnsSqsLambdaChainStack(app, 'S3SnsSqsLambdaChainStack')
EC2InstanceStack(app, "Ec2Stack")
LambdaWithKinesisTrigger(app, "LambdaWithKinesisTrigger")
KinesisS3(app, 'KinesisS3')

app.synth()
