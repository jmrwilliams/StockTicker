import json
import requests
import os
from datetime import datetime

def lambda_handler(event, context):
    ticker = event.get('queryStringParameters', {}).get('ticker', '').upper()
    if not ticker:
        return {'statusCode': 400, 'body': json.dumps({'error': 'ticker parameter required'})}
    
    try:
        financials = get_financials(ticker)
        competitive_analysis = get_competitive_analysis(ticker)
        sec_summary = get_sec_summary(ticker)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'ticker': ticker,
                'financials': financials,
                'competitive_analysis': competitive_analysis,
                'sec_summary': sec_summary
            })
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def get_financials(ticker):
    # Google Finance API endpoint
    url = f'https://www.google.com/finance/quote/{ticker}:NASDAQ'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Alternative: Use Yahoo Finance API as Google Finance doesn't have public API
    yahoo_url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=defaultKeyStatistics,financialData,summaryDetail'
    response = requests.get(yahoo_url, headers=headers)
    data = response.json()
    
    result = data.get('quoteSummary', {}).get('result', [{}])[0]
    financial_data = result.get('financialData', {})
    summary_detail = result.get('summaryDetail', {})
    key_stats = result.get('defaultKeyStatistics', {})
    
    return {
        'market_cap': str(summary_detail.get('marketCap', {}).get('raw', 'N/A')),
        'pe_ratio': str(summary_detail.get('trailingPE', {}).get('raw', 'N/A')),
        'revenue': str(financial_data.get('totalRevenue', {}).get('raw', 'N/A')),
        'profit_margin': str(financial_data.get('profitMargins', {}).get('raw', 'N/A')),
        'debt_to_equity': str(financial_data.get('debtToEquity', {}).get('raw', 'N/A'))
    }

def get_competitive_analysis(ticker):
    # Get company profile from Yahoo Finance
    url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=assetProfile,summaryProfile'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
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