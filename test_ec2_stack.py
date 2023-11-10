import boto3
import pytest
import os
import aws_cdk as core
from cdk.ec2_stack import EC2InstanceStack

# Replace these with your LocalStack service endpoint and region
LOCALSTACK_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"


@pytest.fixture
def ec2_client():
    return boto3.client("ec2", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)

@pytest.fixture
def iam_client():
    return boto3.client("iam", endpoint_url=LOCALSTACK_ENDPOINT, region_name=AWS_REGION)


@pytest.fixture
def app():
    # Create a CDK app and stack
    cdk_output_dir = "cdk.out"

    app = core.App()
    EC2InstanceStack(app, "Ec2Stack")

    # Deploy the CDK stack
    app.synth()
    os.system(f"cdklocal deploy -a {cdk_output_dir} Ec2Stack")
    yield app


def test_ec2(app, ec2_client):
    vpcs = ec2_client.describe_vpcs()
    # print(vpcs)
    # print('----')
    vpc_names = []
    for v in vpcs.get('Vpcs'):
        for tag in v.get('Tags'):
            if tag['Key'] == 'Name':
                vpc_names.append(tag['Value'])

    expected_vpc_name = 'ec2_stack_vpc'
    assert expected_vpc_name in vpc_names

def test_iam_role(iam_client):
    role = iam_client.list_roles()
    roles = [r['RoleName'] for r in role['Roles']]

    expected_iam_role = 'InstanceSSMRole'
    assert expected_iam_role in roles
