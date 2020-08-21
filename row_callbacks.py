from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
import pandas as pd
from config import CONSUMER_KEY
import requests
import json
from options_service import get_stock_quote, get_option_chain

class OptionProcessor():
    def __init__(self, column_names):
        self.column_names = column_names

    @abstractmethod
    # Todo: simplify api - contains all info to compare all options but can be more compactly represented
    def run(self, contract, strike, expiration_date, stock_data, option_chain, days, call_put):
        pass

class OptionChain():
    def __init__(self, tickers, option_processor: OptionProcessor):
        self._option_processor = option_processor

    @property
    def option_processor(self) -> OptionProcessor:
        return self._option_processor

    @option_processor.setter
    def option_processor(self, option_processor: OptionProcessor):
        self.option_processor = option_processor

    def apply(self, ticker_list, column_names, verbose=True):
        all_dfs = []
        now = datetime.now()
        counter = 1
        for ticker_name in ticker_list:
            if verbose:
                print(f"Processing {ticker_name} ({counter}/{len(ticker_list)})")
            counter += 1
            stock_data = get_stock_quote(ticker_name)
            option_chain = get_option_chain(ticker_name)

            put_exp_date_map = option_chain["putExpDateMap"]
            call_exp_date_map = option_chain["callExpDateMap"]

            data = []

            expiration_date_key_list = put_exp_date_map.keys()
            for expiration_date_key in expiration_date_key_list:
                expiration_date = expiration_date_key.split(":")[0]
                exp_date = datetime.strptime(expiration_date, "%Y-%m-%d")
                diff = exp_date - now
                days = diff.days

                # Iterate over Puts
                strikes = put_exp_date_map[expiration_date_key]
                strike_keys = strikes.keys()
                for strike_key in strike_keys:
                    contract_list = strikes[strike_key]
                    for contract in contract_list:
                        row = self.option_processor.run(contract=contract,
                                              strike=strike_key,
                                              expiration_date=expiration_date,
                                              stock_data=stock_data,
                                              option_chain=option_chain,
                                              call_put="PUT")
                        if row:
                            data.append(row)

                # Iterate over Calls
                strikes = call_exp_date_map[expiration_date_key]
                strike_keys = strikes.keys()
                for strike_key in strike_keys:
                    contract_list = strikes[strike_key]
                    for contract in contract_list:
                        row = self.option_processor.run(contract=contract,
                                              strike=strike_key,
                                              expiration_date=expiration_date,
                                              stock_data=stock_data,
                                              option_chain=option_chain,
                                              call_put="CALL")
                        if row:
                            data.append(row)

            result = pd.DataFrame(
                data=data,
                columns=self.option_processor.column_names,
            )
            all_dfs.append(result)
        final_result = pd.concat(all_dfs)
        return final_result

