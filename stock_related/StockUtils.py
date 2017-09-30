
#Import some stuff
import csv
import pandas as pd

csvfile = open('../dataset/stock_price_data.csv')

spamreader = csv.reader(csvfile, delimiter=',')

for row in spamreader:
    if 'date' in row:
        continue
    print(row)
    break

csvfile.close()
