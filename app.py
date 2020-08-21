__author__ = "Marc J Kirschner"
__copyright__ = "Copyright (C) 2020 Marc J Kirschner"
__license__ = "Public Domain"
__version__ = "0.1.1rc"

from flask import Flask
from flask import request

app = Flask(__name__)

from options_service import get_put_info

@app.route('/sellputs/')
def sell_puts():
    tickers = request.args.get('tickers')
    investment = request.args.get('investment')
    tickers_list = list(map(str.upper,tickers.split(",")))
    data, _ = get_put_info(tickers_list, float(investment))
    return data
