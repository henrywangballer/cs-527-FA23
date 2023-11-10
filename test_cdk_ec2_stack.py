import aws_cdk as cdk
from aws_cdk.assertions import Template

from cdk.ec2_stack import EC2InstanceStack

def test_cdk_api_stack():
    app = cdk.App()

    api_stack = EC2InstanceStack(app, "Ec2Stack")

    template = Template.from_stack(api_stack)

    # template.resource_count_is("AWS::IAM::Role", 1)
    template.has_resource("AWS::IAM::Role", {
        "Properties": {"RoleName": "InstanceSSMRole"}
    })

    template.has_resource("AWS::EC2::VPC", {
        "Properties": {"Tags": [
             {
              "Key": "Name",
              "Value": "ec2_stack_vpc"
             }
            ]}
    })


    template.has_resource("AWS::EC2::InternetGateway", {
        "Properties": {
            "Tags": [
             {
              "Key": "Name",
              "Value": "ec2_stack_vpc"
             }
            ]
           }
    })

    template.has_resource("AWS::EC2::Instance", {
        "Properties": {"InstanceType": "t3.nano", "Tags": [
         {
          "Key": "Name",
          "Value": "ec2_stack_instance"
         }
        ]}
    })

