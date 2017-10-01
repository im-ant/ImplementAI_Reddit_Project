from flask import Flask, render_template
import flask
import pandas as pd
import json

app = Flask(__name__)
categoryNames = []
companyDict = {}
companyDictStr = ""

def load_constituents():
    constituents_path = "../dataset/constituents.csv"
    global table
    table = pd.read_csv(constituents_path)
    gb = table.groupby('Sector')
    groups = gb.groups
    for key in groups.keys():
        dict = gb["Symbol", "Name"].get_group(key).reset_index().to_dict()
        categoryNames.append(str(key))
        #print()
        companyDict[str(key)] = list(zip(list(dict["Symbol"].values()), list(dict["Name"].values())))
    global companyDictStr
    companyDictStr = json.dumps(companyDict)
    print(companyDictStr)
    categoryNames.sort()
    pass

@app.route('/')
def index():
    #return flask.jsonify(companyDict)
    #companyDictStr = flask.jsonify(companyDict)
    return render_template("stockviewer.html",companyDictStr = companyDictStr, categoryNames = categoryNames )

if __name__ == '__main__':
    load_constituents()
    app.run()