from aws_cdk import (
    aws_lambda as lambda_,
    aws_kinesis as kinesis,
    aws_lambda_event_sources as event_sources,
    App, Arn, ArnComponents, Duration, Stack
)


class LambdaWithKinesisTrigger(Stack):
    def __init__(self, app: App, id: str) -> None:
        super().__init__(app, id)

        with open("./lambda/kinesis-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        kinesis_stream = kinesis.Stream(
            self, 'KinesisStream',
            stream_name='KinesisStream',
            shard_count=1
        )

        lambdaFn = lambda_.Function(
            self, 'Singleton',
            handler='index.main',
            function_name='kinesisLambda',
            code=lambda_.InlineCode(handler_code),
            runtime=lambda_.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(300)
        )

        kinesis_stream.grant_read(lambdaFn)

        kinesis_event_source = event_sources.KinesisEventSource(
            stream=kinesis_stream,
            starting_position=lambda_.StartingPosition.LATEST,
            batch_size=1
        )

        # Attach the new Event Source To Lambda
        lambdaFn.add_event_source(kinesis_event_source)



