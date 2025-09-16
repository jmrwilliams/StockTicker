# Stock Ticker Serverless App

Serverless AWS application that analyzes stock tickers with financials, competitive analysis, and SEC filing summaries.

## Setup

1. Install AWS SAM CLI and configure AWS credentials
2. Deploy: `chmod +x deploy.sh && ./deploy.sh`

## Usage

```bash
curl 'https://YOUR_API_ENDPOINT/analyze?ticker=AMZN'
```

## Response Format

```json
{
  "ticker": "AMZN",
  "financials": {
    "market_cap": "1500000000000",
    "pe_ratio": "45.2",
    "revenue": "574000000000"
  },
  "competitive_analysis": {
    "sector": "Consumer Discretionary",
    "industry": "Internet Retail"
  },
  "sec_summary": {
    "latest_10k_date": "2024-02-01",
    "summary": "Latest 10-K filing dated 2024-02-01"
  }
}
```

## Architecture

- **Lambda**: Python 3.13 function for stock analysis
- **API Gateway**: REST endpoint
- **External APIs**: Yahoo Finance (financials), SEC EDGAR (filings)