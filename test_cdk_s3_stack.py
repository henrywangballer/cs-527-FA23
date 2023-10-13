import aws_cdk as cdk
from aws_cdk.assertions import Template

from cdk.s3_stack import S3Stack

def test_cdk_s3_stack():
    app = cdk.App()

    s3_stack = S3Stack(app, "MyS3Stack")

    template = Template.from_stack(s3_stack)

    template.resource_count_is("AWS::S3::Bucket", 2)
    template.has_resource("AWS::S3::Bucket", {
        "Properties": {"BucketName": "mybucket"}
    })
    template.has_resource("AWS::S3::Bucket", {
        "Properties": {"BucketName": "mybucket1"}
    })

    # template.has_resource("AWS::S3::Bucket", {
    #     "Properties": {"BucketName": "mybucket2"}
    # })


