from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_s3 as s3
)
from constructs import Construct
from config.env_config import StackEnvConfig

class tdpBucketManagerCDK(Stack):

    def __init__(self, scope: Construct, construct_id: str, config: StackEnvConfig, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        terraform_state_bucket = s3.Bucket(
            self,
            "TerraformStateBucket",
            bucket_name = config.terraform_bucket_name,
            versioned = True,
            removal_policy = RemovalPolicy.DESTROY
        )
        CfnOutput(
            self,
            "TerraformStateBucketName",
            value = terraform_state_bucket.bucket_name
        )
        CfnOutput(
            self,
            "TerraformStateBucketARN",
            value = terraform_state_bucket.bucket_arn
        )
        self.template_options.description = f"{config.project_name} - {config.environment} stack"