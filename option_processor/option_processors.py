from datetime import datetime
from option_processor import OptionProcessor

class PremiumToCollateralPutProcessor(OptionProcessor):
    def __init__(self, column_names, collateral, ignore_itm=True):
        super().__init__(column_names)
        self.collateral = collateral
        self.ignore_itm = ignore_itm


    def run(self, ticker_name, contract, strike, expiration_date, stock_data, option_chain):
        now = datetime.now()
        exp_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        diff = exp_date - now
        # Ameritrade expiration date is 1 day before actual expiration date
        days = diff.days + 1

        if contract["putCall"] == "CALL":
            return None
        else:
            strike = float(strike)
            bid = contract["bid"]
            num_contracts = int(self.collateral / (strike * 100))
            premium = num_contracts * bid * 100
            income_per_day = \
                round((premium / days) if days > 0 else premium, 2)
            in_the_money = contract["inTheMoney"]
            if self.ignore_itm and in_the_money:
                return None
            else:
                return [
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
