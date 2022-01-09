import sys
import pandas as pd
import numpy as np
import openpyxl
from datetime import date as dt, timedelta
from helper import *

date = dt.today() 
df = pd.read_excel('../data/src-data.xlsx')

df['Duration (Hours)'] = (df['Minutes']/60)



study_session = input_request("How long (in minutes) do you want to study each day?: ")



while True:
    is_pomodoro = input('Do you want to schedule using the pomodoro technique? (y/n): ')
    
    if is_pomodoro.lower() in ['y', 'yes', 1, 'true']:
        study_duration = input_request("How long (in minutes) do you want to study for during each pomodoro session?: ")
        break_duration = input_request("How long (in minutes) do you want the break to be?: ")
        study_block = study_duration + break_duration
        
        if study_block > study_session:
            print("\n The pomodoro session cannot be longer than the total study session \n")
            continue
        break
    
    elif is_pomodoro.lower() in ['n', 'no', 0, 'false']:
        study_block = input_request("How long (in minutes) do you want to study for each session?: ")
        break
    else:
        print("\n Please enter y/n \n")


# Schedules topics into the user's defined study_session length
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

# print(df)
#Splits Duration (Hours) column into study blocks (pomodoro sessions)
df = study_block_splitter(df, study_duration)    

print(df)
# Schedules topics into the user's defined study block length
sum = 0
index = 0

while index < len(df):
    
    sum += df.loc[index, 'Duration (Hours)']

    if sum == study_duration:
        sum = 0
    elif sum > study_duration:
        pomodoro_scheduler(df, sum, index, study_duration)
        df = df.sort_index().reset_index(drop=True)
        sum = 0
        df['Duration (Hours)'] = df['Duration (Hours)'].round(5)
    
    index += 1

df['Study Block Summation (Minutes)'] = df['Duration (Hours)'].cumsum()*60

print(df)


#Pomodoro Sessions
df['Pomodoro Session'] = df['Study Block Summation (Minutes)'].apply(lambda x: np.floor(x/(60*study_block)))

# print(df)

# Column names with Name and Date removed
reduced_column_names = [ elem for elem in df.columns.tolist() if elem not in ['Name', 'Date']]

df =df[['Name','Date'] + reduced_column_names]



#Convert duration column to minutes
df.rename(columns={'Duration (Hours)': 'Study Block (Minutes)'}, inplace=True)
df['Study Block (Minutes)'] = df['Study Block (Minutes)'].apply(lambda x: x*60)
# print(df)
try:
    with pd.ExcelWriter("../data/result.xlsx", engine="openpyxl", mode="w", on_sheet_exists="replace") as writer:
        df.to_excel(writer, index=False)
    print("Schedule is ready for viewing")
except:
    #Improve error message
    print("Error - please try run app again")