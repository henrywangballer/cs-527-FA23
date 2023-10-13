from aws_cdk import (
    App,
    Stack,
    aws_s3 as s3
)
from constructs import Construct

class S3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        bucket = s3.Bucket(self, "MyBucket", bucket_name="mybucket")
        bucket1 = s3.Bucket(self, "MyBucket1", bucket_name="mybucket1")

#
# app = App()
# S3Stack(app, "S3Stack")
# app.synth()