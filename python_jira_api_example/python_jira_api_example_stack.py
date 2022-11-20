from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
)


class PythonJiraApiExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines an AWS Lambda resource
        jira_access = _lambda.Function(
            self, 'JiraAccessHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('jira_lambda'),
            handler='jira_access.handler',
        )

        fn_url = jira_access.add_function_url()
        CfnOutput(
            scope=self,
            id="jiraAccessUrl",
            value=fn_url.url,
        )

        # Defines an AWS Lambda resource
        jira_webhook = _lambda.Function(
            self, 'JiraWebhookHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('jira_lambda'),
            handler='jira_webhook.handler',
        )

        fn_url2 = jira_webhook.add_function_url(auth_type=_lambda.FunctionUrlAuthType.NONE)
        CfnOutput(
            scope=self,
            id="jiraWebhookUrl",
            value=fn_url2.url,
        )