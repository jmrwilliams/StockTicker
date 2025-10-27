#!/usr/bin/env python3
import json
from lambda_function import lambda_handler

# Test the Lambda function locally
event = {
    'queryStringParameters': {'ticker': 'AMZN'}
}

result = lambda_handler(event, {})
print(json.dumps(json.loads(result['body']), indent=2))