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

    study_session = input_request("How long (in minutes) do you want to study each day?: ")


    #Getting the total study Datetime and pomodoro splits
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


    #Getting the time to study each day
    while True:
        try:
            
            print("What date would you like to start study? \n")
            study_date = datetime.strptime(input('Please specify the date in the dd/mm/yyyy format: '), "%d/%m/%Y")
            
            print("What time would you like to start studying each day? \n")
            study_time = datetime.strptime(input('Please specify the time in the HH:MM (24 hour) format: '), "%H:%M")

            break
        except:
            print ("Please enter the specified format\n")
            continue



    #Datetime object
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

    print(df[['Name', 'Date', 'Pomodoro Session', 'Start Time', 'End Time']])

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