from flask import Flask
from flask import request

app = Flask(__name__)

from tda_options import get_put_info

@app.route('/sellputs/')
def sell_puts():
    tickers = request.args.get('tickers')
    investment = request.args.get('investment')
    tickers_list = list(map(str.upper,tickers.split(",")))
    data, _ = get_put_info(tickers_list, float(investment))
    return data

# app.run(host='0.0.0.0', port='5372')