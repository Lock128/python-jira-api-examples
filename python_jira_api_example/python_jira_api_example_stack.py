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

        queue = sqs.Queue(
            self, "PythonJiraApiExampleQueue",
            visibility_timeout=Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "PythonJiraApiExampleTopic"
        )

        topic.add_subscription(subs.SqsSubscription(queue))
        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'JiraAccessHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('jira_lambda'),
            handler='jira_access.handler',
        )

        fn_url = my_lambda.add_function_url()
        CfnOutput(
            scope=self,
            id="funcURLOutput",
            value=fn_url.to_string(),
        )