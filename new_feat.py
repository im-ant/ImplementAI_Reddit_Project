import pandas as pd

prices = pd.read_csv("../../dataset/stock_price_data.csv")
prices['date'] = pd.to_datetime(prices['date'])

def prev_fluc(date, company_tick):
    """Given company tick name and date, return fluctuation of last date"""
    price = prices[[date,company_tick]]
    try:
        index = price.index[price['date']==date][0]
    except:
        print("Not a trading day. Tracing back...")
        while not len(price.index[price['date']==date]):
            date = pd.to_datetime(date)-pd.to_timedelta(1,unit='d') # trace back one day
    index = price.index[price['date']==date][0]
    cur_price = price.loc[index-2][company_tick]
    prev_price = price.loc[index-1][company_tick]
    return (cur_price - prev_price)/prev_price
