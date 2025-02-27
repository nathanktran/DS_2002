import yfinance as yf
import pandas as pd
import requests

def fetch_stock_data(tickers, apikey):
    url = "https://yfapi.net/v6/finance/quote"
    params = {"symbols": ",".join(tickers)}
    headers = {"x-api-key": apikey}  
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print("Error fetching stock data:", response.json())
        return []
    data = response.json().get('quoteResponse', {}).get('result', [])
    stock_data = []
    for stock in data:
        stock_data.append({
            "Stock Ticker": stock.get("symbol", "N/A"),
            "Company Name": stock.get("longName", "N/A"),
            "Current Market Price": format_currency(stock.get('regularMarketPrice'))
        })
    return stock_data

def fetch_additional_data(tickers, module, apikey):
    additional_data = []
    for ticker in tickers:
        url = f"https://yfapi.net/v11/finance/quoteSummary/{ticker}"
        params = {"modules": module}
        headers = {"x-api-key": apikey}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching data for {ticker}: {response.json()}")
            continue
        data = response.json().get("quoteSummary", {}).get("result", [{}])[0]
        module_data = data.get(module, {})
        formatted_data = {
            "Stock Ticker": ticker,
            "52 Week High": format_currency(module_data.get("fiftyTwoWeekHigh")),
            "52 Week Low": format_currency(module_data.get("fiftyTwoWeekLow")),
            "ROA": format_percentage(module_data.get("returnOnAssets"))
        }
        additional_data.append(formatted_data)
    return pd.DataFrame(additional_data)

def get_trending_stocks(apikey):
    url = "https://yfapi.net/v1/finance/trending/US"
    headers = {"x-api-key": apikey}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error fetching trending stocks:", response.json())
        return pd.DataFrame()
    trending = response.json().get("finance", {}).get("result", [{}])[0].get("quotes", [])
    trending_tickers = [stock["symbol"] for stock in trending[:10]]
    trending_data = []
    for ticker in trending_tickers:
        stock_info = fetch_stock_data([ticker], apikey)[0]
        extra_data = fetch_additional_data([ticker], "summaryDetail", apikey)
        if not extra_data.empty:
            stock_info["52 Week High"] = extra_data.iloc[0]["52 Week High"]
            stock_info["52 Week Low"] = extra_data.iloc[0]["52 Week Low"]
        trending_data.append(stock_info)
    return pd.DataFrame(trending_data)

def format_currency(value):
    if isinstance(value, dict) and "raw" in value:  
        return f"${value['raw']:,.2f}"  
    return "N/A" if value is None else value

def format_percentage(value):
    if isinstance(value, dict) and "raw" in value:
        return f"{value['raw'] * 100:.2f}%"
    return "N/A"

def main():
    apikey = input("Enter your API Key: ")  
    symbols = input("Enter stock symbols separated by commas: ").split(',')
    symbols = [s.strip().upper() for s in symbols]
    stock_data = fetch_stock_data(symbols, apikey)
    print("\nBasic Stock Data:")
    for data in stock_data:
        print(f"Stock Ticker: {data['Stock Ticker']}, Company: {data['Company Name']}, Current Market Price: {data['Current Market Price']}")
    module = input("\nChoose a module (summaryDetail, financialData, defaultKeyStatistics, earnings): ").strip()
    additional_data = fetch_additional_data(symbols, module, apikey)
    print("\nAdditional Data (52 Week High, 52 Week Low, ROA):")
    print(additional_data.to_string(index=False))
    trending_stocks = get_trending_stocks(apikey)
    print("\nTrending Stocks:")
    for _, row in trending_stocks.iterrows():
        print(f"Stock Ticker: {row['Stock Ticker']}, Company: {row['Company Name']}, Current Market Price: {row['Current Market Price']}, 52 Week High: {row['52 Week High']}, 52 Week Low: {row['52 Week Low']}")

if __name__ == "__main__":
    main()
