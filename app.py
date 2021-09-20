#!/usr/bin/env python3
import os
from aws_cdk import core
from infrastructure.LambdaStack.LambdaStack import CdkLambdaStack


app = core.App()
CdkLambdaStack(app, "LambdaStack",
    env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    )

app.synth()
