__author__ = "Marc J Kirschner"
__copyright__ = "Copyright (C) 2020 Marc J Kirschner"
__license__ = "Public Domain"
__version__ = "0.1.1rc"

from datetime import datetime
import pandas as pd
import requests
import json
import option_processor as OptionProcessor
from option_processor.option_processors import PremiumToCollateralPutProcessor
from tda import get_stock_quote, get_option_chain

"""
apply callback create_row_func to the option chain and return a dataframe 
where each row of the dataframe is created by create_row_func. The dataframe's
column names are specified by column_names

Args:
    ticker_list: csv of ticker names
    create_row_func: callback that takes an option contract and returns a row 
    param3: array of column names in the returned dataframe.

Returns:
    Dataframe representing the processed option chains of the stocks provided through ticker_list 

Raises:
    KeyError: Raises an exception.
"""
#
def apply(ticker_list, create_row_func, column_names, verbose=True):
    all_dfs = []
    now = datetime.now()
    counter = 1
    for ticker_name in ticker_list:
        if verbose:
            print(f"Processing {ticker_name} ({counter}/{len(ticker_list)})")
        counter += 1
        stock_data = get_stock_quote(ticker_name)
        option_chain = get_option_chain(ticker_name)
        expiration_date_key_list = put_exp_date_map.keys()

        put_exp_date_map = option_chain["putExpDateMap"]
        call_exp_date_map = option_chain["callExpDateMap"]


        data = []


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
                    row = create_row_func(contract=contract,
                                          strike=strike_key,
                                          expiration_date=expiration_date,
                                          stock_data=stock_data,
                                          option_chain=option_chain,
                                          call_put="PUT")
                    data.append(row)

            # Iterate over Calls
            strikes = call_exp_date_map[expiration_date_key]
            strike_keys = strikes.keys()
            for strike_key in strike_keys:
                contract_list = strikes[strike_key]
                for contract in contract_list:
                    row = create_row_func(contract=contract,
                                          strike=strike_key,
                                          expiration_date=expiration_date,
                                          stock_data=stock_data,
                                          option_chain=option_chain,
                                          call_put="CALL")
                    data.append(row)


        result = pd.DataFrame(
            data=data,
            columns=column_names,
        )
        all_dfs.append(result)
    final_result = pd.concat(all_dfs)
    return final_result


def get_put_info_2(ticker_list, investment):
    column_names = [
                "Ticker",
                "Expiration",
                "Days",
                "Strike",
                "Premium",
                "IncomePerDay",
                "Num_Contracts",
                "Bid",
                "InTheMoney",
            ]
    premium_to_collateral_put_processor = PremiumToCollateralPutProcessor(
        column_names=column_names,
        collateral=investment)
    option_chain = OptionProcessor.OptionChain(ticker_list, premium_to_collateral_put_processor)
    df = option_chain.process()
    final_result = df.sort_values(by=["IncomePerDay"], ascending=False)
    data = final_result.to_csv()
    return data, final_result


# Find high premium / collateral puts
def get_put_info(ticker_list, investment, ignore_in_the_money=True, verbose=True):
    column_names = [
        "Ticker",
        "Expiration",
        "Days",
        "Strike",
        "Premium",
        "IncomePerDay",
        "Num_Contracts",
        "Bid",
        "InTheMoney",
    ]
    premium_to_collateral_put_processor = PremiumToCollateralPutProcessor(
        column_names=column_names,
        collateral=investment)
    option_chain = OptionProcessor.OptionChain(ticker_list, premium_to_collateral_put_processor)
    df = option_chain.process()
    final_result = df.sort_values(by=["IncomePerDay"], ascending=False)
    data = final_result.to_csv()
    return data, final_result
    # all_dfs = []
    # now = datetime.now()
    # counter = 1
    # for ticker_name in ticker_list:
    #     if verbose:
    #         print(f"Processing {ticker_name} ({counter}/{len(ticker_list)})")
    #     counter += 1
    #     stock_data = get_stock_quote(ticker_name)
    #     current_price = stock_data[ticker_name]["lastPrice"]
    #     option_chain = get_option_chain(ticker_name)
    #     put_exp_date_map = option_chain["putExpDateMap"]
    #     expiration_date_key_list = put_exp_date_map.keys()
    #
    #     data = []
    #
    #     for expiration_date_key in expiration_date_key_list:
    #         expiration_date = expiration_date_key.split(":")[0]
    #         exp_date = datetime.strptime(expiration_date, "%Y-%m-%d")
    #         diff = exp_date - now
    #         days = diff.days
    #
    #         strikes = put_exp_date_map[expiration_date_key]
    #         strike_keys = strikes.keys()
    #         for strike_key in strike_keys:
    #             contract_list = strikes[strike_key]
    #             for contract in contract_list:
    #                 if contract["putCall"] == "CALL":
    #                     pass
    #                 else:
    #                     strike = float(strike_key)
    #                     bid = contract["bid"]
    #                     # ask = contract["ask"]
    #                     num_contracts = investment / (strike * 100)
    #                     premium = num_contracts * bid * 100
    #                     income_per_day = premium / days
    #                     in_the_money = contract["inTheMoney"]
    #                     if ignore_in_the_money and in_the_money:
    #                         continue
    #                     if in_the_money:
    #                         # TODO: Problem: Incorrect calculation
    #                         stock_assigned = num_contracts * 100
    #                         cost = stock_assigned * strike
    #                         current_value = stock_assigned * current_price
    #                         profit = current_value - cost
    #                         profit_per_day = profit / days
    #                         income_per_day += profit_per_day
    #
    #                     data.append(
    #                         [
    #                             ticker_name,
    #                             expiration_date,
    #                             days,
    #                             strike,
    #                             premium,
    #                             income_per_day,
    #                             num_contracts,
    #                             bid,
    #                             in_the_money,
    #                         ]
    #                     )
    #
    #     result = pd.DataFrame(
    #         data=data,
    #         columns=[
    #             "Ticker",
    #             "Expiration",
    #             "Days",
    #             "Strike",
    #             "Premium",
    #             "IncomePerDay",
    #             "Num_Contracts",
    #             "Bid",
    #             "InTheMoney",
    #         ],
    #     )
    #     all_dfs.append(result)
    # final_result = pd.concat(all_dfs)
    # final_result = final_result.sort_values(by=["IncomePerDay"], ascending=False)
    # data = final_result.to_csv()
    # return data, final_result

# Calculate Max Pain
def get_max_pain():
    pass
