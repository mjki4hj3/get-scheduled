#Helper Functions
from pandas.core.frame import DataFrame


def round_to_minimum_duration(value, study_block):
    if value < study_block:
        value = study_block
    else:
        value = 1
    return value

# function to split oversized topics into defined study periods
def splitting_function(index, sum, max_duration, column_to_split, df):
    
    # scheduling the oversized topic with remaining space in current study period
    space = max_duration - (sum - df.loc[index,column_to_split])
    
    excess = df.at[index, column_to_split] - space
    df.at[index, column_to_split] = space # scheduling the oversized topic with remainder time
    
    # splitting the remainder of the oversized topic 
    slot = 0.01
    # splitting oversized into as many study slots equal to defined studyperiod 
    while excess > max_duration:
        df.loc[index + slot] = df.loc[index]
        df.loc[(index + slot), column_to_split] = max_duration
        excess = excess - max_duration
        slot+= 0.01

    # scheduling the remainder of the oversized topic
    df.loc[index + slot] = df.loc[index]
    df.loc[(index + slot), column_to_split] = excess


    return df




def study_block_splitter(df, study_duration):

    index = 0
    slot = 0.01 
    
    while index < len(df):

        if df.loc[index, "Minutes"] > study_duration:

            split = df.loc[index, "Minutes"] - study_duration
            df.loc[index, "Minutes"] = study_duration
            df.loc[index + slot] = df.loc[index]
            df.loc[(index + slot), "Minutes"] = split
            df = df.sort_index().reset_index(drop=True)
            slot += 0.01
            

        index += 1

    return df




def pomodoro_scheduler(df, sum, index, study_duration):

    slot = 0.01
    space = study_duration - (sum - df.loc[index, "Minutes"])
    # print(f"Space: {space}")
    df.loc[index, "Minutes"] = space
    excess = sum - study_duration
    df.loc[(index + slot)] = df.loc[index]
    df.loc[(index + slot), "Minutes"] = excess

    return df




def input_request(message): 
    if message == "How long (in hours) do you want to study each day?: ":
        while True:
            try:
                max_duration = float(input(message))
                if max_duration > 0:
                    break
                elif max_duration == 0:
                    print("Please enter a non-zero study duration")
                    continue
                else:
                    print("Please enter a non-negative study duration")
                    continue
            except:
                print("Please enter a number")
                continue
            
        return max_duration*60
    
    else:
        while True:
            try:
                max_duration = float(input(message))
                if max_duration > 0:
                    break
                elif max_duration == 0:
                    print("Please enter a non-zero study duration")
                    continue
                else:
                    print("Please enter a non-negative study duration")
                    continue
            except:
                print("Please enter a number")
                continue
            
        return max_duration