__author__ = "Marc J Kirschner"
__copyright__ = "Copyright (C) 2020 Marc J Kirschner"
__license__ = "Public Domain"
__version__ = "0.1.1rc"

from datetime import datetime
import pandas as pd
from config import CONSUMER_KEY
import requests
import json

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


# Find high premium / collateral puts
def get_put_info(ticker_list, investment, ignore_in_the_money=True, verbose=True):
    all_dfs = []
    now = datetime.today()
    counter = 1
    for ticker_name in ticker_list:
        if verbose:
            print(f"Processing {ticker_name} ({counter}/{len(ticker_list)})")
        counter += 1
        stock_data = get_stock_quote(ticker_name)
        current_price = stock_data[ticker_name]["lastPrice"]
        option_chain = get_option_chain(ticker_name)
        put_exp_date_map = option_chain["putExpDateMap"]
        expiration_date_key_list = put_exp_date_map.keys()

        data = []

        for expiration_date_key in expiration_date_key_list:
            expiration_date = expiration_date_key.split(":")[0]
            diff = expiration_date_key.split(":")[1]
            days= int(diff)

            strikes = put_exp_date_map[expiration_date_key]
            strike_keys = strikes.keys()
            for strike_key in strike_keys:
                contract_list = strikes[strike_key]
                for contract in contract_list:
                    if contract["putCall"] == "CALL":
                        pass
                    else:
                        strike = float(strike_key)
                        bid = contract["bid"]
                        # ask = contract["ask"]
                        num_contracts = int(investment / (strike * 100))
                        premium = num_contracts * bid * 100
                        income_per_day = \
                            round((premium / days) if days > 0 else premium, 2)
                        in_the_money = contract["inTheMoney"]
                        if ignore_in_the_money and in_the_money:
                            continue
                        if in_the_money:
                            # TODO: Problem: Incorrect calculation
                            stock_assigned = num_contracts * 100
                            cost = stock_assigned * strike
                            current_value = stock_assigned * current_price
                            profit = current_value - cost
                            profit_per_day = profit / days
                            income_per_day += profit_per_day

                        data.append(
                            [
                                ticker_name,
                                expiration_date,
                                days,
                                strike,
                                premium,
                                income_per_day,
                                num_contracts,
                                bid,
                                in_the_money,
                            ]
                        )

        result = pd.DataFrame(
            data=data,
            columns=[
                "Ticker",
                "Expiration",
                "Days",
                "Strike",
                "Premium",
                "IncomePerDay",
                "Num_Contracts",
                "Bid",
                "InTheMoney",
            ],
        )
        all_dfs.append(result)
    final_result = pd.concat(all_dfs)
    final_result = final_result.sort_values(by=["IncomePerDay"], ascending=False)
    data = final_result.to_csv()
    return data, final_result

