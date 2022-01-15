import sys
import os
import pandas as pd
import numpy as np
import openpyxl
from datetime import date as dt, timedelta, datetime
from helper import *

date = dt.today() 

def prepare_dataframe():

    df = pd.read_excel('../data/src-data.xlsx')
    study_session = input_request("How long (in hours) do you want to study each day?: ")


    #Getting the total study Datetime and pomodoro splits
    while True:

        study_duration = input_request("How long (in minutes) do you want to study for during each pomodoro session?: ")
        break_duration = input_request("How long (in minutes) do you want the break to be?: ")
        study_block = study_duration + break_duration
        
        if study_block > study_session:
            print("\n The pomodoro session cannot be longer than the total study session \n")
            continue
        break



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


    # study_session = 30
    # study_duration = 30
    # break_duration = 0
    # study_block = study_duration + break_duration
    
    # study_date = datetime.strptime('11/01/2022', "%d/%m/%Y")
    # study_time= datetime.strptime('13:00', "%H:%M")
    
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

   
    '''
    Splitting topics into study durations
    '''
    sum = 0
    index = 0
    
    while index < len(df):
        
        sum += df.loc[index, 'Minutes']
        
       
        if sum == study_duration:
            sum = 0
        elif sum > study_duration:
            df = pomodoro_scheduler(df, sum, index, study_duration)
            sum = 0

        df = df.sort_index().reset_index(drop=True)  
        index += 1
        
    #Splits Minutes column into study blocks (pomodoro sessions)
    df = study_block_splitter(df, study_duration)    


    '''
    Cummulatively summing minutes column
    '''
    
    df['Study Block Summation (Minutes)'] = df['Minutes'].cumsum()
    
    '''
    Pomodorotion sessions count
    '''
    
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

    '''
    Adding in start, end and break times
    '''
    df.loc[0, 'Start Time'] = study_date_time
    df.loc[0, 'End Time'] =  study_date_time + timedelta(minutes=study_duration)
    df.loc[0, 'Break Time'] =  df.loc[0, 'End Time'] + timedelta(minutes=break_duration)
    previous_date = df.loc[0, 'Date'].date()

    index = 1

    while index < len(df):
        previous_date = df.loc[index-1, 'Date'].date()

        if previous_date < df.loc[index, 'Date'].date():
            #Next day
            df.loc[index, 'Start Time'] = df.loc[index, 'Date']
            df.loc[index, 'End Time'] = df.loc[index, 'Date'] + timedelta(minutes=study_duration)
            df.loc[index, 'Break Time'] = df.loc[index, 'End Time'] + timedelta(minutes=break_duration)
        
        else:    
            #Same day
            if df.loc[index, 'Pomodoro Session'] - df.loc[index-1, 'Pomodoro Session'] == 0:
                #Same Pomodoro Session
                df.loc[index, 'Start Time'] = df.loc[index-1, 'Start Time']
                df.loc[index, 'End Time'] = df.loc[index-1, 'End Time']
                df.loc[index, 'Break Time'] = df.loc[index-1, 'Break Time']
            else:
                #New Pomodoro Session
                df.loc[index, 'Start Time'] = df.loc[index-1, 'Break Time']
                df.loc[index, 'End Time'] = df.loc[index, 'Start Time'] + timedelta(minutes=study_duration)
                df.loc[index, 'Break Time'] = df.loc[index, 'End Time'] + timedelta(minutes=break_duration)
        
        index +=1
        

    # Column names with Name and Date removed
    reduced_column_names = [ elem for elem in df.columns.tolist() if elem not in ['Name', 'Date']]

    df =df[['Name','Date'] + reduced_column_names]

    
    #Modified df for excel output
    df_for_excel = df.copy()
    
    df_for_excel['Date'] = pd.to_datetime(df_for_excel['Date'])
    df_for_excel['Start Time'] = pd.to_datetime(df_for_excel['Start Time'])
    df_for_excel['End Time'] = pd.to_datetime(df_for_excel['End Time'])
    df_for_excel['Break Time'] = pd.to_datetime(df_for_excel['Break Time'])
    
    df_for_excel['Date'] = df_for_excel['Date'].dt.date
    df_for_excel['Start Time'] = df_for_excel['Start Time'].dt.time
    df_for_excel['End Time'] = df_for_excel['End Time'].dt.time
    df_for_excel['Break Time'] = df_for_excel['Break Time'].dt.time


    try:
        with pd.ExcelWriter("../data/result.xlsx", engine="openpyxl", mode="w", on_sheet_exists="replace") as writer:
            df_for_excel.to_excel(writer, index=False)
        print("Calendar is being populated ...")
    except:
        #Improve error message
        print("Error - please try run app again")
    
    return df

if __name__ == '__main__':
    prepare_dataframe()
