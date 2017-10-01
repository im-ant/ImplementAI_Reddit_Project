
#Import some stuff
import sys, csv
import pandas as pd
import numpy as np

STOCK_PRICE_DATA = "/data/ImplementReddit/dataset/stock_price_data.csv"
UNLABELLED_DATA = sys.argv[1]
OUTPUT_DATA = sys.argv[2]


#Load the input csv file as a dataframe
stock_df = pd.DataFrame.from_csv('/data/ImplementReddit/dataset/stock_price_data.csv')
		
#Get the pricing  values in numpy
stock_np = stock_df.drop('date', axis=1).values

#Take the differences in numpy
change = (stock_np[:-1] -stock_np[1:]) / stock_np[:-1]

#Create new dataframe with the company headers
change_df = pd.DataFrame(change, columns=stock_df.columns.values[1:])

#Concatenate the date into the dataframe
change_df['date'] = stock_df['date']

#print(change_df)


#Load the training data dataset (to be labelled)
unlab_df = pd.DataFrame.from_csv(UNLABELLED_DATA)

print(unlab_df)

#List to store values
perc_change_list = []

#Indeces and row counter
idx = 0
empty_date_list = []

#Iterate over all rows of the unlabelled data
for index, row in unlab_df.iterrows():
	#Get the row in the financial data with the correct date
	change_row = change_df.loc[change_df['date'] == row['date'] ]
	#Check the row is not empty
	if change_row.empty:
		empty_date_list.append(idx)
		idx += 1
		continue
	
	#Get the right company and its percentage change
	perc_change_value = change_row[ row['company'] ].values[0]
	#Add to list
	perc_change_list.append(perc_change_value)
	idx += 1

print(empty_date_list)	
#Delete the rows with no indeces
unlab_df.drop(unlab_df.index[empty_date_list ], inplace=True )

#Turn list into new column in dataframe
unlab_df['target'] = np.asarray(perc_change_list)

print(unlab_df)

#Output dataframe to a csv
unlab_df.to_csv(OUTPUT_DATA)
print("Done!")


