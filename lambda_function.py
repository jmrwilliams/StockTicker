import json
import requests
import os
from datetime import datetime

def lambda_handler(event, context):
    # Handle both direct invocation and API Gateway
    query_params = event.get('queryStringParameters') or {}
    ticker = query_params.get('ticker', '').upper() if query_params else ''
    
    if not ticker:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'ticker parameter required'})
        }
    
    try:
        financials = get_financials(ticker)
        competitive_analysis = get_competitive_analysis(ticker)
        sec_summary = get_sec_summary(ticker)
        
        response_body = {
            'ticker': ticker,
            'financials': financials,
            'competitive_analysis': competitive_analysis,
            'sec_summary': sec_summary
        }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response_body)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

def get_financials(ticker):
    # Yahoo Finance API
    url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=defaultKeyStatistics,financialData,summaryDetail'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        result = data.get('quoteSummary', {}).get('result', [{}])[0]
        financial_data = result.get('financialData', {})
        summary_detail = result.get('summaryDetail', {})
        
        def safe_get(data_dict, key, default='N/A'):
            value = data_dict.get(key, {})
            return str(value.get('raw', default)) if isinstance(value, dict) else str(default)
        
        return {
            'market_cap': safe_get(summary_detail, 'marketCap'),
            'pe_ratio': safe_get(summary_detail, 'trailingPE'),
            'revenue': safe_get(financial_data, 'totalRevenue'),
            'profit_margin': safe_get(financial_data, 'profitMargins'),
            'debt_to_equity': safe_get(financial_data, 'debtToEquity')
        }
    except Exception as e:
        return {'error': f'Failed to fetch financials: {str(e)}'}

def get_competitive_analysis(ticker):
    url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=assetProfile'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        result = data.get('quoteSummary', {}).get('result', [{}])[0]
        profile = result.get('assetProfile', {})
        
        sector = profile.get('sector', 'Unknown')
        industry = profile.get('industry', 'Unknown')
        
        return {
            'sector': sector,
            'industry': industry,
            'pe_vs_sector': 'Analysis requires sector benchmark data',
            'market_position': f'Company operates in {industry} sector'
        }
    except Exception as e:
        return {'error': f'Failed to fetch competitive analysis: {str(e)}'}

def get_sec_summary(ticker):
    # SEC EDGAR API for 10-K filings
    headers = {'User-Agent': 'StockAnalyzer contact@example.com'}
    
    # Get company CIK
    url = f'https://www.sec.gov/files/company_tickers.json'
    response = requests.get(url, headers=headers)
    companies = response.json()
    
    cik = None
    for company in companies.values():
        if company['ticker'].upper() == ticker:
            cik = str(company['cik_str']).zfill(10)
            break
    
    if not cik:
        return {'error': 'Company not found in SEC database'}
    
    # Get recent 10-K filing
    url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    response = requests.get(url, headers=headers)
    data = response.json()
    
    filings = data.get('filings', {}).get('recent', {})
    forms = filings.get('form', [])
    dates = filings.get('filingDate', [])
    
    latest_10k = None
    for i, form in enumerate(forms):
        if form == '10-K':
            latest_10k = dates[i]
            break
    
    return {
        'latest_10k_date': latest_10k,
        'summary': f'Latest 10-K filing dated {latest_10k}' if latest_10k else 'No recent 10-K found',
        'note': 'Full text analysis requires additional processing'
    }