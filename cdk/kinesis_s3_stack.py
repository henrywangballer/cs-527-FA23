from aws_cdk import (
    aws_lambda as lambda_,
    aws_kinesis as kinesis,
    aws_dynamodb,
    aws_s3 as s3,
    aws_iam as iam,
    aws_kinesisfirehose as firehose,
    aws_lambda_event_sources as event_sources,
    App, Arn, ArnComponents, Duration, Stack
)

from constructs import Construct


class KinesisS3(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # kinesis_table = aws_dynamodb.Table(
        #     self, "kinesis_table",
        #     table_name='kinesis_table',
        #     partition_key=aws_dynamodb.Attribute(
        #         name="id",
        #         type=aws_dynamodb.AttributeType.STRING
        #     )
        # )

        kinesis_stream = kinesis.Stream(
            self, 'KinesisStream',
            stream_name='KinesisStream',
            shard_count=1
        )

        bucket = s3.Bucket(self, "kinesisbucket", bucket_name="kinesisbucket")
        bucket_arn = bucket.bucket_arn


        firehose_role = iam.Role(self, "MyFirehoseRole",
             role_name='firehoseRole',
             assumed_by=iam.ServicePrincipal("firehose.amazonaws.com"),
             managed_policies=[
                 iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
                 iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
             ]
         )

        # stream = firehose.DeliveryStream(self, "MyStream",
        #     destinations=[destinations.S3Bucket(bucket)],
        #     delivery_stream_name='kinesis-firehose-stream',
        #     role=firehose_role,
        #     source_stream=kinesis_stream
        # )

        print(f'{kinesis_stream.stream_arn}')

        stream = firehose.CfnDeliveryStream(self, "MyStream",
            delivery_stream_name="firehose-stream",
            s3_destination_configuration=firehose.CfnDeliveryStream.S3DestinationConfigurationProperty(
                bucket_arn=bucket_arn,
                role_arn=firehose_role.role_arn
            ),
            kinesis_stream_source_configuration=firehose.CfnDeliveryStream.KinesisStreamSourceConfigurationProperty(
                kinesis_stream_arn=kinesis_stream.stream_arn,
                role_arn=firehose_role.role_arn
            )
        )
