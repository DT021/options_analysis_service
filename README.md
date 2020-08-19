# Ameritrade Configuration
This service makes requests to Ameritrades API. So you must sign up for a developer
account with Ameritrade, and follow their guidlines for setting up an app. Once you have
setup an app there will be a corresponding Consumer Key. This key needs to be pasted into
config.py
`CONSUMER_KEY = 'CHANGEME' in order for ameritrade to authenticate the requests.

IMPORTANT: Do not store your consumer key in version control. It is a highly secure private key that gives
access to your ameritrade account. 


# Installation
`pip install -r requirements.txt`

# Run Command Line Utility
`download.py <tickerlist> <investment> <filename>`

## Example
`download.py riot,lvs,gold 10000 list.csv`

This will write a csv file called list.csv in the current working directory
populated with data pulled from the option chains of the stocks provided.
It will use $10,000 as the amount of available collateral to sort the stocks
in descending order according to the premium/collateral ratio when selling puts.

### Example of output

```
,Ticker,Expiration,Days,Strike,Premium,IncomePerDay,Num_Contracts,Bid,InTheMoney
6,RIOT,2020-08-21,1,3.5,285.7142857142858,285.7142857142858,28.571428571428573,0.1,False
21,CWH,2020-08-21,1,36.0,166.66666666666666,166.66666666666666,2.7777777777777777,0.6,False
```

# Run Web Service

An endpoint /sellputs exposes this data to http requests. Just run app.py in a flask container and then
submit GET requests as in the following example:
`http://localhost:5000/sellputs?tickers=f,hal&investment=10000`
