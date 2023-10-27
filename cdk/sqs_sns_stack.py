from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_events,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_sns as sns,
    aws_sns_subscriptions as sns_subs,
    aws_sqs as sqs,
)
from constructs import Construct


class S3SnsSqsLambdaChainStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id)

        # lambda_dir = kwargs["lambda_dir"]
        LAMBDA_TIMEOUT = 30

        # Note: A dead-letter queue is optional but it helps capture any failed messages
        dlq = sqs.Queue(
            self,
            id="dead_letter_queue_id",
            queue_name="dead_letter_queue",
            retention_period=Duration.days(7)
        )
        dead_letter_queue = sqs.DeadLetterQueue(
            max_receive_count=1,
            queue=dlq
        )

        upload_queue = sqs.Queue(
            self,
            id="sample_queue_id",
            queue_name="upload_queue",
            dead_letter_queue=dead_letter_queue,
            visibility_timeout=Duration.seconds(LAMBDA_TIMEOUT * 6)
        )

        sqs_subscription = sns_subs.SqsSubscription(
            upload_queue,
            raw_message_delivery=True
        )

        upload_event_topic = sns.Topic(
            self,
            id="sample_sns_topic_id",
            topic_name="sns_upload_topic"
        )

        # This binds the SNS Topic to the SQS Queue
        upload_event_topic.add_subscription(sqs_subscription)

        # Note: Lifecycle Rules are optional but are included here to keep costs
        #       low by cleaning up old files or moving them to lower cost storage options
        s3_bucket = s3.Bucket(
            self,
            id="sample_bucket_id",
            bucket_name="sns-bucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            lifecycle_rules=[
                s3.LifecycleRule(
                    enabled=True,
                    expiration=Duration.days(365),
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                            transition_after=Duration.days(30)
                        ),
                        s3.Transition(
                            storage_class=s3.StorageClass.GLACIER,
                            transition_after=Duration.days(90)
                        ),
                    ]
                )
            ]
        )


        s3_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED_PUT,
            s3n.SnsDestination(upload_event_topic),
            s3.NotificationKeyFilter(prefix="uploads", suffix=".csv")
        )

        function = _lambda.Function(self, "lambda_function",
                                    runtime=_lambda.Runtime.PYTHON_3_10,
                                    handler="sns-sqs-handler.handler",
                                    function_name='sqs_sns_lambda',
                                    code=_lambda.Code.from_asset(path="./lambda"),
                                    timeout=Duration.seconds(LAMBDA_TIMEOUT)
                                    )

        # This binds the lambda to the SQS Queue
        invoke_event_source = lambda_events.SqsEventSource(upload_queue)
        function.add_event_source(invoke_event_source)

