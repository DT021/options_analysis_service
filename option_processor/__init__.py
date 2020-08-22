from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
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


class OptionProcessor():
    def __init__(self, column_names: List):
        self.column_names = column_names

    @abstractmethod
    def run(self, ticker_name, contract, strike, expiration_date, stock_data, option_chain):
        pass


class OptionChain():
    def __init__(self, ticker_list, option_processor: OptionProcessor):
        self._ticker_list = ticker_list
        self._option_processor = option_processor

    @property
    def option_processor(self) -> OptionProcessor:
        return self._option_processor

    @option_processor.setter
    def option_processor(self, option_processor: OptionProcessor):
        self.option_processor = option_processor

    def process(self, verbose=True):
        all_dfs = []
        counter = 1

        for ticker_name in self._ticker_list:
            if verbose:
                print(f"Processing {ticker_name} ({counter}/{len(self._ticker_list)})")
            counter += 1
            stock_data = get_stock_quote(ticker_name)
            option_chain = get_option_chain(ticker_name)

            put_exp_date_map = option_chain["putExpDateMap"]
            call_exp_date_map = option_chain["callExpDateMap"]

            data = []

            expiration_date_key_list = put_exp_date_map.keys()
            for expiration_date_key in expiration_date_key_list:
                expiration_date = expiration_date_key.split(":")[0]

                # Iterate over Puts
                strikes = put_exp_date_map[expiration_date_key]
                strike_keys = strikes.keys()
                for strike_key in strike_keys:
                    contract_list = strikes[strike_key]
                    for contract in contract_list:
                        row = self.option_processor.run(ticker_name,
                                              contract=contract,
                                              strike=strike_key,
                                              expiration_date=expiration_date,
                                              stock_data=stock_data,
                                              option_chain=option_chain)
                        if row:
                            data.append(row)

                # Iterate over Calls
                strikes = call_exp_date_map[expiration_date_key]
                strike_keys = strikes.keys()
                for strike_key in strike_keys:
                    contract_list = strikes[strike_key]
                    for contract in contract_list:
                        row = self.option_processor.run(ticker_name,
                                             contract=contract,
                                              strike=strike_key,
                                              expiration_date=expiration_date,
                                              stock_data=stock_data,
                                              option_chain=option_chain)
                        if row:
                            data.append(row)

            result = pd.DataFrame(
                data=data,
                columns=self.option_processor.column_names,
            )
            all_dfs.append(result)
        final_result = pd.concat(all_dfs)
        return final_result

