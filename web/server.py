from flask import Flask, render_template
import flask
import pandas as pd
import json
import datetime

app = Flask(__name__)
categoryNames = []
companyDict = {}
companyDictStr = ""
stockPriceDict = {}
stockPriceDictStr = ""
companySymbols = []
predictionDict = {}
predictionDictStr = ""

def load_constituents():
    constituents_path = "../dataset/constituents.csv"
    table = pd.read_csv(constituents_path)
    gb = table.groupby('Sector')
    groups = gb.groups
    global companySymbols
    companySymbols = table["Symbol"].tolist()
    for key in groups.keys():
        dict = gb["Symbol", "Name"].get_group(key).reset_index().to_dict()
        categoryNames.append(str(key))
        #print()
        companyDict[str(key)] = list(zip(list(dict["Symbol"].values()), list(dict["Name"].values())))
    global companyDictStr
    companyDictStr = json.dumps(companyDict)
    #print(companyDictStr)
    categoryNames.sort()
    pass

def load_stock_prices():
    stock_prices_path = "../dataset/stock_price_data.csv"
    table = pd.read_csv(stock_prices_path)
    #print(table.head())
    #startDate = datetime.date(2017,4,1)
    #startDate = '2017-04-10'
    #endDate = datetime.date(2017,4,18)
    startIndex = 571
    endIndex = 576
    #endDate = '2017-04-18'
    #table['date'] = pd.to_datetime(table.date)
    #table.set_index(['date'], inplace=True)
    #filteredByDate = table[(table["date"] >= startDate) & (table["date"] <= endDate)]
    filteredByDate = table.loc[startIndex:endIndex, :]
   # if 'date' in filteredByDate.columns:
    #    print('date was there before dropping NaNs')
    filteredByDate = filteredByDate.dropna(axis=1, how='any')
    #if 'date' in filteredByDate.columns:
    #    print('date was there after dropping NaNs')
    #print(filteredByDate)

    symbolsToRemove = []
    stockPriceDict['date'] = filteredByDate['date'].tolist()
    for sym in companySymbols:
        if sym in filteredByDate.columns:
            stockPriceDict[sym] = filteredByDate[sym].tolist()
        else:
            symbolsToRemove.append(sym)

    global stockPriceDictStr
    stockPriceDictStr = json.dumps(stockPriceDict)

    #print(stockPriceDictStr)
    pass

def load_predictions():
    predictions_path = "../company_prediction.csv"
    table = pd.read_csv(predictions_path)
    gb = table.groupby('company')
    groups = gb.groups

    for key in groups.keys():
        dict = gb["prediction"].get_group(key).tolist()
        predictionDict[key] = dict


    global predictionDictStr
    predictionDictStr = json.dumps(predictionDict)

    pass

@app.route('/')
def index():
    #return flask.jsonify(companyDict)
    #companyDictStr = flask.jsonify(companyDict)
    return render_template("stockviewer.html",companyDictStr = companyDictStr, categoryNames = categoryNames,
                           stockPriceDictStr = stockPriceDictStr, predictionDictStr = predictionDictStr )

if __name__ == '__main__':
    load_constituents()
    load_stock_prices()
    load_predictions()
    app.run(host='0.0.0.0')