from aws_cdk import (
    core,
    aws_sam as sam,
    aws_lambda as _lambda,
    aws_iam as _iam
)
from aws_cdk.core import Tags
POWERTOOLS_BASE_NAME = 'AWSLambdaPowertools'
# Find latest from github.com/awslabs/aws-lambda-powertools-python/releases
POWERTOOLS_VER = '1.17.0'
POWERTOOLS_ARN = 'arn:aws:serverlessrepo:eu-west-1:057560766410:applications/aws-lambda-powertools-python-layer'


class CdkLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:

        super().__init__(scope, id, **kwargs)

        #Create role
        lambda_role = _iam.Role(scope=self, id='cdk-lambda-role',
                                assumed_by =_iam.ServicePrincipal('lambda.amazonaws.com'),
                                role_name='cdk-lambda-role',
                                managed_policies=[
                                _iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaVPCAccessExecutionRole'),
                                _iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaBasicExecutionRole')
                                ])
        powertools_app = sam.CfnApplication(self,
            f'{POWERTOOLS_BASE_NAME}Application',
            location={
                'applicationId': POWERTOOLS_ARN,
                'semanticVersion': POWERTOOLS_VER
            },
        )

        powertools_layer_arn = powertools_app.get_att("Outputs.LayerVersionArn").to_string()
        powertools_layer_version = _lambda.LayerVersion.from_layer_version_arn(self, f'{POWERTOOLS_BASE_NAME}', powertools_layer_arn)

        # Defines an AWS Lambda resource
        cdk_lambda = _lambda.Function(
            self, 'cdk-sample-lambda',
            runtime=_lambda.Runtime.PYTHON_3_7,
            function_name='cdk-sample-lambda',
            description='Lambda function deployed using AWS CDK Python',
            code=_lambda.Code.asset('src/functions'),
            tracing=_lambda.Tracing.ACTIVE,
            handler='sample.handler',
            role=lambda_role,
            layers=[powertools_layer_version],
            environment={
                'NAME': 'cdk-sample-lambda',
                'ENV': 'dev',
            }
        )

        # Adding Tags to Lambda

        Tags.of(cdk_lambda).add("Owner", "harshit9715@gmail.com")


        #Output of created resource
        core.CfnOutput(scope=self, id='cdk-lambda-stack-output',
                       value=cdk_lambda.function_name)
