from constructs import Construct
from aws_cdk import (
    App, Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigw,
    aws_iam as _iam
)


class ApiCorsLambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_iam_role = _iam.Role(self, 'LambdaRole',
              assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
              role_name='LambdaRole',
              managed_policies=[
                  _iam.ManagedPolicy.from_aws_managed_policy_name(
                      'service-role/AWSLambdaBasicExecutionRole')
              ]
        )

        base_api = _apigw.RestApi(self, 'ApiGatewayWithCors',
                                  rest_api_name='ApiGatewayWithCors')

        base_lambda = _lambda.Function(self, 'ApiCorsLambda',
                                       function_name='ApiCorsLambda',
                                       handler='lambda-handler.handler',
                                       role=lambda_iam_role,
                                       runtime=_lambda.Runtime.PYTHON_3_9,
                                       code=_lambda.Code.from_asset('./lambda'))


        example_entity = base_api.root.add_resource(
            'example',
            default_cors_preflight_options=_apigw.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=_apigw.Cors.ALL_ORIGINS)
        )
        example_entity_lambda_integration = _apigw.LambdaIntegration(
            base_lambda,
            proxy=False,
            integration_responses=[
                _apigw.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )
        example_entity.add_method(
            'GET', example_entity_lambda_integration,
            method_responses=[
                _apigw.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    }
                )
            ]
        )

        example1_entity = base_api.root.add_resource(
            'example1',
            default_cors_preflight_options=_apigw.CorsOptions(
                allow_methods=['GET', 'OPTIONS'],
                allow_origins=_apigw.Cors.ALL_ORIGINS)
        )

        qp_lambda = _lambda.Function(self, 'QueryParamsLambda',
                                       function_name='QueryParamsLambda',
                                       handler='qp-lambda-handler.handler',
                                       role=lambda_iam_role,
                                       runtime=_lambda.Runtime.PYTHON_3_9,
                                       code=_lambda.Code.from_asset('./lambda'))


        qp_lambda_integration = _apigw.LambdaIntegration(
            qp_lambda,
            proxy=True,
            integration_responses=[
                _apigw.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                )
            ]
        )

        this_validator = base_api.add_request_validator(
            "example-validator",
            request_validator_name="example-validator",
            validate_request_parameters=True,
            validate_request_body=False
        )
        example1_entity.add_method(
            'GET', qp_lambda_integration,
            request_parameters={
                'method.request.querystring.message': True
            },
            request_validator=this_validator,
            method_responses=[
                _apigw.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True
                    },
                ),
            ]
        )



#
# app = App()
# ApiCorsLambdaStack(app, "ApiCorsLambdaStack")
# app.synth()