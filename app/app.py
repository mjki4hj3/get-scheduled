import sys
import pandas as pd
import numpy as np
import openpyxl
from datetime import date as dt, timedelta
from helper import *

df = pd.read_excel('../data/src-data.xlsx')

df['Duration (Hours)'] = df['Minutes']/60

#Set values that are less than the minimum study session duration
df['Duration (Hours)'].update(df.loc[df['Duration (Hours)'] < 0.5, ['Duration (Hours)']]['Duration (Hours)'].apply(lambda x: round_to_minimum_duration(x)))

#Get the remainder for durations bigger than minimum study session duration
values_greater_minimum_duration = df.loc[df['Duration (Hours)'] > 0.5, ['Duration (Hours)']]['Duration (Hours)'].apply(lambda x: x % 1).values.tolist()

#Call the minimum duration function
updated_values = []

for value in values_greater_minimum_duration:
    updated_values.append(round_to_minimum_duration(value))

#Take the integer and add it to the minimum duration (rounded or otherwise)
integer_values = df.loc[df['Duration (Hours)'] > 0.5, ['Duration (Hours)']]['Duration (Hours)'].astype('int').values.tolist()

updated_duration = [a+b for a, b in zip(integer_values, updated_values)]

# List of the index position of the durations that need updating
indexes = df.loc[df['Duration (Hours)'] > 0.5, ['Duration (Hours)']].index

position = 0
for index in indexes:
    df.at[index, 'Duration (Hours)'] =  updated_duration[position]
    position += 1


date = dt.today() 

# add input validation
while True:
    
    try:
        study_period = float(input("How long (in hours) do you want each study session per day to be?: "))
        if study_period > 0:
            break
        elif study_period == 0:
            print("Please enter a non-zero study duration")
            continue
        else:
            print("Please enter a non-negative study duration")
            continue
    except:
        print("Please enter a number")
        continue
        
    
sum = 0
index = 0 
while index < len(df):
    
    sum += df.at[index, 'Duration (Hours)']
    
    if sum < study_period:
        df.loc[index,"Date"] = date
    elif sum == study_period:
        df.loc[index,"Date"] = date
        date = date + timedelta(hours=1)
        sum = 0 
    else:
        splitting_function(index, sum, study_period, df)
        df = df.sort_index().reset_index(drop=True)
        df.loc[index, "Date"] = date
        date = date + timedelta(hours=1)
        sum = 0   
        ```
    index +=1  

# Moving the date column 
cols = df.columns.tolist()
cols =  cols[0:1] + cols[-1:] + cols[1:3]
df = df[cols]


with pd.ExcelWriter("../data/result.xlsx", engine="openpyxl", mode="w", on_sheet_exists="replace") as writer:
   df.to_excel(writer, index=False)