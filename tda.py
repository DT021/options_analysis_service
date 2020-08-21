import requests
import json
from config import CONSUMER_KEY

# Ameritrade API Endpoint
# Stock Info
def get_endpoint(ticker):
    base_url = (
        "https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}"
    )
    endpoint = base_url.format(stock_ticker=ticker)
    return endpoint


# Option Chain
def get_option_chain(ticker):
    endpoint = get_endpoint(ticker)
    page = requests.get(url=endpoint, params={"apikey": CONSUMER_KEY})
    content = json.loads(page.content)
    return content


# Obtain price of stock
def get_stock_quote(ticker):
    endpoint = "https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?"
    full_url = endpoint.format(stock_ticker=ticker)
    page = requests.get(url=full_url, params={"apikey": CONSUMER_KEY})
    content = json.loads(page.content)
    return content
