#!/bin/bash

echo "=== Testing Lambda Function Locally ==="
python3 test_local.py

echo -e "\n=== Testing with SAM Local API ==="
echo "Starting local API server..."
echo "Test with: curl 'http://127.0.0.1:3000/analyze?ticker=AMZN'"
sam local start-api