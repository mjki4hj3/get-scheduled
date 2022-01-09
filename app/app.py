import sys
import os
import pandas as pd
import numpy as np
import openpyxl
from datetime import date as dt, timedelta, datetime
from helper import *

date = dt.today() 
df = pd.read_excel('../data/src-data.xlsx')

# df['Duration (Hours)'] = (df['Minutes'])



# study_session = input_request("How long (in hours) do you want to study each day?: ")



def prepare_dataframe():
        
    df = pd.read_excel('../data/src-data.xlsx')

   # df['Duration (Hours)'] = df['Minutes']/60

    study_session = input_request("How long (in hours) do you want to study each day?: ")


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

        sum += df.at[index, 'Minutes']

        if sum < study_session:
            df.loc[index,"Date"] = new_date
        elif sum == study_session:
            df.loc[index,"Date"] = new_date
            new_date = new_date + timedelta(days=1)
            sum = 0 
        else:
            splitting_function(index, sum, study_session, 'Minutes', df)
            df = df.sort_index().reset_index(drop=True)
            df.loc[index, "Date"] = new_date
            new_date = new_date + timedelta(days=1)
            sum = 0   
            
        index +=1  

    # Splits Duration (Hours) column into study blocks (pomodoro sessions)
    # df = study_block_splitter(df, study_block)    


    # df['Study Block Summation (Minutes)'] = df['Minutes'].cumsum()

    # #Pomodoro Sessions
    # df['Pomodoro Session'] = df['Study Block Summation (Minutes)'].apply(lambda x: np.floor(x/(study_block)))

   
    #Splits Duration (Hours) column into study blocks (pomodoro sessions)
    df = study_block_splitter(df, study_duration)    

    # Schedules topics into the user's defined study block length
    sum = 0
    index = 0
    
   
    # print(f"Study_duration: {study_duration}")  
    while index < len(df):
        
        sum += df.loc[index, 'Minutes']
        
        # print(f"sum: {sum}")
        if sum == study_duration:
            sum = 0
        elif sum > study_duration:
            df = pomodoro_scheduler(df, sum, index, study_duration)
            df = df.sort_index().reset_index(drop=True)
            sum = 0
            #df['Duration (Hours)'] = df['Duration (Hours)'].round(5)
        
        index += 1

        '''
        Formating Data Frame
        '''
    print(df)

    
    df['Study Block Summation (Minutes)'] = df['Minutes'].cumsum()
    
    
    index = 1
    df.loc[0, "Pomodoro Session"] = 1
    while index < len(df):
        if df.loc[index,'Study Block Summation (Minutes)'] % study_duration == 0:
            if df.loc[index, "Minutes"] == study_duration:
                df.loc[index, "Pomodoro Session"] = df.loc[(index - 1), "Pomodoro Session"] + 1
            else:
                df.loc[index, "Pomodoro Session"] = df.loc[(index - 1), "Pomodoro Session"] 

        else:
            df.loc[index, "Pomodoro Session"] = np.ceil(df.loc[index, 'Study Block Summation (Minutes)']/study_duration)

        index += 1


    #Pomodoro Sessions
    # df['Pomodoro Session'] = df['Study Block Summation (Minutes)'].apply(lambda x: np.floor(x/(study_duration)))

   

    df.loc[0, 'Start Time'] = study_date_time
    df.loc[0, 'End Time'] =  study_date_time + timedelta(minutes=study_duration)
    previous_date = df.loc[0, 'Date'].date()

    index = 1


    while index < len(df):
        previous_date = df.loc[index-1, 'Date'].date()
        
        #if its the next date
        if previous_date < df.loc[index, 'Date'].date():
            #Next day
            print("Next day")
            df.loc[index, 'Start Time'] = df.loc[index, 'Date']
            df.loc[index, 'End Time'] = df.loc[index, 'Date'] + timedelta(minutes=study_duration)
        
        else:    
            #Same day
            if df.loc[index, 'Pomodoro Session'] - df.loc[index-1, 'Pomodoro Session'] == 0:
                #Same Pomodoro Session
                
                df.loc[index, 'Start Time'] = df.loc[index-1, 'Start Time']
                df.loc[index, 'End Time'] = df.loc[index-1, 'End Time']
            else:
                #New Pomodoro Session
                df.loc[index, 'Start Time'] = df.loc[index-1, 'End Time']
                df.loc[index, 'End Time'] = df.loc[index, 'Start Time'] + timedelta(minutes=study_duration)
        
        index +=1
        

    # Column names with Name and Date removed
    reduced_column_names = [ elem for elem in df.columns.tolist() if elem not in ['Name', 'Date']]

    df =df[['Name','Date'] + reduced_column_names]


    #Convert duration column to minutes and rename to study block minutes
    df.rename(columns={'Minutes': 'Study Block (Minutes)'}, inplace=True)
    #df['Study Block (Minutes)'] = df['Study Block (Minutes)'].apply(lambda x: x*60)

    print(df[['Name', 'Date', 'Study Block Summation (Minutes)', 'Pomodoro Session', 'Start Time', 'End Time']])

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
