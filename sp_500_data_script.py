import pandas as pd
import quandl
from functools import reduce
API_KEY = 'E6pn_k56yxs6SfxgLvTA'
quandl.ApiConfig.api_key = API_KEY
#
df = pd.read_csv('dataset/constituents.csv')

list_of_ticker = []

for symbol in df['Symbol'].values.tolist():
    try:
        data = quandl.get_table('WIKI/PRICES', qopts={'columns': ['date', 'close']}, ticker=symbol,
                            date={'gte': '2015-01-01', 'lte': '2017-09-01'})
        data = data.rename(columns={'close': symbol})
        list_of_ticker.append(data)
    except:
        print(symbol)

list_of_ticker = reduce(lambda x, y: pd.merge(x, y, on='date', how='outer'), list_of_ticker)
list_of_ticker.to_csv('stock_price_data.csv')

