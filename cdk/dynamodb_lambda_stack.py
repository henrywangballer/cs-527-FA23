from aws_cdk import (
    aws_lambda,
    aws_dynamodb,
    aws_events,
    aws_events_targets,
    Duration, Stack,
    aws_iam as _iam
)
from constructs import Construct

class DynamodbLambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create dynamo table
        demo_table = aws_dynamodb.Table(
            self, "demo_table",
            table_name='demo_table',
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )

        lambda_iam_role = _iam.Role(self, 'LambdaRole',
            assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name='LambdaRole',
            managed_policies=[
                _iam.ManagedPolicy.from_aws_managed_policy_name(
                    'service-role/AWSLambdaBasicExecutionRole')
            ]
        )

        # create producer lambda function
        producer_lambda = aws_lambda.Function(self, "producer_lambda_function",
                                              runtime=aws_lambda.Runtime.PYTHON_3_10,
                                              function_name='producer_lambda_function',
                                              handler="producer-lambda_handler",
                                              role=lambda_iam_role,
                                              code=aws_lambda.Code.from_asset("./lambda"))

        producer_lambda.add_environment("TABLE_NAME", demo_table.table_name)

        # grant permission to lambda to write to demo table
        demo_table.grant_write_data(producer_lambda)

        # create consumer lambda function
        consumer_lambda = aws_lambda.Function(self, "consumer_lambda_function",
                                              runtime=aws_lambda.Runtime.PYTHON_3_10,
                                              function_name='consumer_lambda_function',
                                              handler="consumer-handler.lambda_handler",
                                              role=lambda_iam_role,
                                              code=aws_lambda.Code.from_asset("./lambda"))

        consumer_lambda.add_environment("TABLE_NAME", demo_table.table_name)

        # grant permission to lambda to read from demo table
        demo_table.grant_read_data(consumer_lambda)

        # create a Cloudwatch Event rule
        one_minute_rule = aws_events.Rule(
            self, "one_minute_rule",
            rule_name='one_minute_rule',
            schedule=aws_events.Schedule.rate(Duration.minutes(1)),
        )

        # Add target to Cloudwatch Event
        one_minute_rule.add_target(aws_events_targets.LambdaFunction(producer_lambda))
        one_minute_rule.add_target(aws_events_targets.LambdaFunction(consumer_lambda))