import sys
import pandas as pd
import numpy as np
import openpyxl
from datetime import date as dt, timedelta
from helper import *

df = pd.read_excel('../data/src-data.xlsx')

df['Duration (Hours)'] = df['Minutes']/60


# study_session = input_request("How long (in minutes) do you want to study each day?: ")

# study_duration = input_request("How long (in minutes) do you want to study for each pomodoro session?: ")
# break_duration = input_request("How long (in minutes) do you want the break to be?: ")


study_session = 120/60
study_duration = 20/60
break_duration = 10/60


study_block = study_duration + break_duration

# #Set values that are less than the minimum study session duration
# df['Duration (Hours)'].update(df.loc[df['Duration (Hours)'] < study_block, ['Duration (Hours)']]['Duration (Hours)'].apply(lambda x: round_to_minimum_duration(x, study_block)))

# #Get the remainder for durations bigger than minimum study session duration
# values_greater_minimum_duration = df.loc[df['Duration (Hours)'] > study_block, ['Duration (Hours)']]['Duration (Hours)'].apply(lambda x: x % 1).values.tolist()

# #Call the minimum duration function
# updated_values = []
# for value in values_greater_minimum_duration:
#     updated_values.append(round_to_minimum_duration(value, study_block))

#Take the integer and add it to the minimum duration (rounded or otherwise)
# integer_values = df.loc[df['Duration (Hours)'] > study_block, ['Duration (Hours)']]['Duration (Hours)'].astype('int').values.tolist()

# updated_duration = [a+b for a, b in zip(integer_values, updated_values)]

# List of the index position of the durations that need updating
# indexes = df.loc[df['Duration (Hours)'] > study_block, ['Duration (Hours)']].index

# position = 0
# for index in indexes:
#     df.at[index, 'Duration (Hours)'] =  updated_duration[position]
#     position += 1


date = dt.today() 
        
    
sum = 0
index = 0 
while index < len(df):

    sum += df.at[index, 'Duration (Hours)']

    if sum < study_session:
        df.loc[index,"Date"] = date
    elif sum == study_session:
        df.loc[index,"Date"] = date
        date = date + timedelta(days=1)
        sum = 0 
    else:
        splitting_function(index, sum, study_session, 'Duration (Hours)', df)
        df = df.sort_index().reset_index(drop=True)
        df.loc[index, "Date"] = date
        date = date + timedelta(days=1)
        sum = 0   
        
    index +=1  

#Splits Duration (Hours) column into study blocks (pomodoro sessions)
df = study_block_splitter(df, study_block)    


df['Study Block Summation (Minutes)'] = df['Duration (Hours)'].cumsum()*60

#Pomodoro Sessions
df['Pomodoro Session'] = df['Study Block Summation (Minutes)'].apply(lambda x: np.floor(x/(60*study_block)))

# Column names with Name and Date removed
reduced_column_names = [ elem for elem in df.columns.tolist() if elem not in ['Name', 'Date']]

df =df[['Name','Date'] + reduced_column_names]



#Convert duration column to minutes
df.rename(columns={'Duration (Hours)': 'Study Block (Minutes)'}, inplace=True)
df['Study Block (Minutes)'] = df['Study Block (Minutes)'].apply(lambda x: x*60)
print(df)
try:
    with pd.ExcelWriter("../data/result.xlsx", engine="openpyxl", mode="w", on_sheet_exists="replace") as writer:
        df.to_excel(writer, index=False)
    print("Schedule is ready for viewing")
except:
    #Improve error message
    print("Error - please try run app again")