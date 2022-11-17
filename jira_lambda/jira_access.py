import csv
import json
import base64
import logging
import requests
import boto3
from http import HTTPStatus
from json.decoder import JSONDecodeError
from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
JIRA_HEADERS = {"Accept": "application/json", "Authorization": ""}

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    global JIRA_HEADERS
    # GET Basic authrization token
    basic_auth_token_jira = base64_encode(
        read_secret("/tool/jira/user"),
        read_secret("/tool/jira/token")
    )
    # Update headers
    JIRA_HEADERS["Authorization"] = f"Basic {basic_auth_token_jira}"
    get_all_jira_issues(event["project_key"], "https://lockhead.atlassian.net/")
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
    }

def read_secret(secret_name):
    logger.info(f"Reading secret from parameter store: {secret_name}")
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name=secret_name, WithDecryption=True)
    logger.info(f"Finished reading secret from parameter store: {len(parameter)}")
    return parameter['Parameter']['Value']

def get_all_jira_issues(project_key, server, query=None):

    start_at = 0
    max_results = 250

    jql= f"project=\"{project_key}\""

    if query:
        logger.info(f"Found query {query}")
        jql = query
    selectedIssues=[]
    while True:
        try:
            response = requests.get(
                url=f"{server}/rest/api/latest/search",
                params={
                    "jql": jql,
                    "startAt": start_at,
                    "maxResults": max_results
                },
                timeout=10,
                headers=JIRA_HEADERS
            )
            if response.status_code == HTTPStatus.OK:
                data = json.loads(response.text)

                issues=len(data['issues'])
                print(f"Found issues: {issues}")
                for issue in data['issues']:
                    logger.info(f"Found issue: {issue['key']}")
                    selectedIssues.append(issue)


                if len(data["issues"]) == 0:
                    break
                start_at += max_results
            else:
                logger.info(f"Error accessing JIRA: {response.status_code}")
        except (KeyError, JSONDecodeError, RequestException) as error:
            logger.exception(error)

    with open('issues.csv', 'w', newline='') as csvfile:
        fieldnames = ['expand', 'key', 'id', 'fields', 'self']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for issue in selectedIssues:
            writer.writerow(issue)
    logger.info("data retrieved succesfully")
    return selectedIssues


def base64_encode(username: str, password: str):
    return base64.b64encode(
        s=f"{username}:{password}".encode("utf-8")
    ).decode("utf-8")

if __name__ == "__main__":
    data = {
        "path": "project_key",
        "project_key": "TTO"
    }
    handler(data, "")