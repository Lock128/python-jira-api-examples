import json
import base64
import logging
import requests
from http import HTTPStatus
from json.decoder import JSONDecodeError
from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
JIRA_HEADERS = {"Accept": "application/json", "Authorization": ""}

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    store_new_issue(event)
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Issue has been safed in database {}\n'.format(event['issue']['key'])
    }

def store_new_issue(event):

    logger.info(f"Saving issue in database: {event['issue']['key']}")