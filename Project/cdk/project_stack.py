from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3
)
from constructs import Construct

class ProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = s3.Bucket(self, "MyBucket")
