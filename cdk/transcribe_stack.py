from constructs import Construct
from aws_cdk import (
    App, Stack, Duration,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
    aws_iam as _iam,
    aws_s3 as s3
)


class TranscribeStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_iam_role = _iam.Role(self, 'TranscribeLambdaRole',
              assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
              role_name='TranscribeLambdaRole',
              managed_policies=[
                  _iam.ManagedPolicy.from_aws_managed_policy_name(
                      'service-role/AWSLambdaBasicExecutionRole',
                  ),
                  _iam.ManagedPolicy.from_aws_managed_policy_name(
                      "AmazonS3FullAccess",
                  ),

              ]
        )


        base_lambda = _lambda.Function(self, 'TranscribeLambda',
                                       function_name='TranscribeLambda',
                                       handler='transcribe-handler.lambda_handler',
                                       role=lambda_iam_role,
                                       runtime=_lambda.Runtime.PYTHON_3_10,
                                       timeout=Duration.seconds(200),
                                       code=_lambda.Code.from_asset('./lambda'))

        input_bucket = s3.Bucket(self, "InputtranscribeBucket", bucket_name="inputtranscribebucket")

