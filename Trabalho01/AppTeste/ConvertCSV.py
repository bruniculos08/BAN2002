import pandas as pd

tsv_file = 'data.tsv'

# reading given tsv file
csv_table=pd.read_table(tsv_file,sep='\t')
 
# converting tsv file into csv
csv_table.to_csv('data.csv',index=False)
 
# output
print("Successfully made csv file")