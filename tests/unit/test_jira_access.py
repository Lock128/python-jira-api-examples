import jira_lambda.jira_access as jira_lambda
import json


def test_jira_access_handler():
    data = {
        "path": "project_key",
        "project_key": "TTO",
    }

    jira_lambda.handler(data, data);