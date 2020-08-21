"""Usage:
  download.py <tickerlist> <investment> <filename> [-o]
  download.py -h | --help | --version
"""

__author__ = "Marc J Kirschner"
__copyright__ = "Copyright (C) 2020 Marc J Kirschner"
__license__ = "Public Domain"
__version__ = "0.1.1rc"

from docopt import docopt
from options_service import get_put_info


# Command Line Utility
def main():
    args = docopt(__doc__, version=__version__)
    ticker_list = list(map(str.upper,args["<tickerlist>"].split(",")))
    investment = float(args["<investment>"])
    filename = args["<filename>"]
    if ".csv" not in filename:
        filename = f"{filename}.csv"

    if args["-o"]:
        verbose = False
    else:
        verbose = True
    put_info_text, put_info_df = get_put_info(ticker_list, investment, verbose=verbose)

    if not args["-o"]:
        put_info_df.to_csv(filename)
        print(put_info_df.head())
    else:
        print(put_info_text)


if __name__ == "__main__":
    main()
