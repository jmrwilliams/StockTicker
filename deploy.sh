#!/bin/bash

# Build and deploy the serverless app
echo "Building and deploying Stock Ticker app..."

# Build the SAM application
sam build

# Deploy with guided prompts (first time)
sam deploy --guided

echo "Deployment complete!"
echo "Test with: curl 'https://YOUR_API_ENDPOINT/analyze?ticker=AMZN'"
echo "Note: Using Yahoo Finance API for financial data"