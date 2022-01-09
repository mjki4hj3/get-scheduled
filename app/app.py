import sys
import os
import pandas as pd
import numpy as np
import openpyxl
from datetime import date as dt, timedelta, datetime
from helper import *




def prepare_dataframe():
        
    df = pd.read_excel('../data/src-data.xlsx')

    df['Duration (Hours)'] = df['Minutes']/60


    study_session = 120/60
    study_duration = 20/60
    study_break = 10/60
    study_block= study_duration + study_break
    study_time = datetime.strptime('13:00', "%H:%M")
    study_date = datetime.strptime('09/01/2022', "%d/%m/%Y")

    study_date_time = study_date.replace(hour=study_time.hour, minute=study_time.minute)


    sum = 0
    index = 0
    new_date = study_date_time

    while index < len(df):

        sum += df.at[index, 'Duration (Hours)']

        if sum < study_session:
            df.loc[index,"Date"] = new_date
        elif sum == study_session:
            df.loc[index,"Date"] = new_date
            new_date = new_date + timedelta(days=1)
            sum = 0 
        else:
            splitting_function(index, sum, study_session, 'Duration (Hours)', df)
            df = df.sort_index().reset_index(drop=True)
            df.loc[index, "Date"] = new_date
            new_date = new_date + timedelta(days=1)
            sum = 0   
            
        index +=1  

    #Splits Duration (Hours) column into study blocks (pomodoro sessions)
    df = study_block_splitter(df, study_block)    


    df['Study Block Summation (Minutes)'] = df['Duration (Hours)'].cumsum()*60

    #Pomodoro Sessions
    df['Pomodoro Session'] = df['Study Block Summation (Minutes)'].apply(lambda x: np.floor(x/(60*study_block)))



    df.loc[0, 'Start Time'] = study_date_time
    df.loc[0, 'End Time'] =  study_date_time + timedelta(hours=study_block)
    previous_date = df.loc[0, 'Date'].date()

    index = 1


    while index < len(df):
        previous_date = df.loc[index-1, 'Date'].date()
        
        #if its the next date
        if previous_date < df.loc[index, 'Date'].date():
            #Next day
            df.loc[index, 'Start Time'] = df.loc[index, 'Date']
            df.loc[index, 'End Time'] = df.loc[index, 'Date'] + timedelta(hours=study_block)
        
        else:
            #Same day
            if df.loc[index, 'Pomodoro Session'] - df.loc[index-1, 'Pomodoro Session'] == 0:
                #Same Pomodoro Session
                df.loc[index, 'Start Time'] = df.loc[index-1, 'Start Time']
                df.loc[index, 'End Time'] = df.loc[index-1, 'End Time']
            else:
                #New Pomodoro Session
                df.loc[index, 'Start Time'] = df.loc[index-1, 'End Time']
                df.loc[index, 'End Time'] = df.loc[index, 'Start Time'] + timedelta(hours=study_block)
        
        index +=1
        


    '''
    Formating Data Frame
    '''

    #Format date column
    df['Date'] = df['Date'].apply(lambda x: x.date())
    
    df['Start Time'] = df['Start Time'].apply(lambda x: x.time())
    df['End Time'] = df['End Time'].apply(lambda x: x.time())
    

    # Moving Name and Date to first and second column position
    reduced_column_names = [ elem for elem in df.columns.tolist() if elem not in ['Name', 'Date']]
    df =df[['Name','Date'] + reduced_column_names]


    #Convert duration column to minutes and rename to study block minutes
    df.rename(columns={'Duration (Hours)': 'Study Block (Minutes)'}, inplace=True)
    df['Study Block (Minutes)'] = df['Study Block (Minutes)'].apply(lambda x: x*60)

    print(df[['Name', 'Date', 'Start Time', 'End Time']])

    try:
        with pd.ExcelWriter("../data/result.xlsx", engine="openpyxl", mode="w", on_sheet_exists="replace") as writer:
            df.to_excel(writer, index=False)
        print("Schedule is ready for viewing")
    except:
        #Improve error message
        print("Error - please try run app again")
    
    return df

if __name__ == '__main__':
    prepare_dataframe()