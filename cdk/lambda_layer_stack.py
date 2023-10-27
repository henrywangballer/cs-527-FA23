from aws_cdk import (
    aws_lambda as _lambda,
    App, RemovalPolicy, Stack,
    aws_iam as _iam
)
from constructs import Construct


class LambdaLayerStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create layer
        layer = _lambda.LayerVersion(self, 'helper_layer',
                                     code=_lambda.Code.from_asset("./layer/python"),
                                     layer_version_name="helper_layer",
                                     description='Common helper utility',
                                     compatible_runtimes=[
                                         _lambda.Runtime.PYTHON_3_8,
                                         _lambda.Runtime.PYTHON_3_9,
                                         _lambda.Runtime.PYTHON_3_10
                                     ],
                                     removal_policy=RemovalPolicy.DESTROY
                                     )

        lambda_iam_role = _iam.Role(self, 'LambdaLayerRole',
            assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name='LambdaLayerRole',
            managed_policies=[
                _iam.ManagedPolicy.from_aws_managed_policy_name(
                    'service-role/AWSLambdaBasicExecutionRole')
            ]
        )

        # create lambda function
        function = _lambda.Function(self, "lambda_function",
                                    runtime=_lambda.Runtime.PYTHON_3_8,
                                    function_name='layer_function',
                                    handler="layer-handler.handler",
                                    role=lambda_iam_role,
                                    code=_lambda.Code.from_asset("./lambda"),
                                    layers=[layer])



# app = App()
# LambdaLayerStack(app, "LambdaLayerExample")
# app.synth()