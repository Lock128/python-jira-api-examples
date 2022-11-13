#!/usr/bin/env python3

import aws_cdk as cdk

from python_jira_api_example.python_jira_api_example_stack import PythonJiraApiExampleStack


app = cdk.App()
PythonJiraApiExampleStack(app, "python-jira-api-example")

app.synth()
