import requests
import json


api_token = 'Enter Here'
api_url_top5 = ('https://pro-api.coinmarketcap.com'
                '/v1/cryptocurrency/quotes/latest?symbol='
                'BTC,'
                'ETH,'
                'BCH,'
                'LTC,'
                'NANO')

head = {
        'X-CMC_PRO_API_KEY': api_token,
        'Content-Type': 'application/json'
        }


def ticker():
    # This just deals with requests and makes shit easier to work with.
    response = requests.get(api_url_top5, headers=head)
    tjson = response.content
    tdata = json.loads(tjson)
    ticker = tdata['data']

    # Iterate over the data that has been delivered and print out goodness.
    for item in ticker:
        name = ticker[item]['name']
        out = ticker[item]['quote']['USD']
        if len(name) > 9:
            name = ticker[item]['symbol']
        # Inside the {}
        # {Index : Padding . Trunk Type}
        # The '.' means trunkate and '<' means align left
        print('{0:9.9s} ${1:<10.2f} 7D {2:+3.2f}%'.format(
              name,
              out['price'],
              out['percent_change_7d']
              ))


test()
