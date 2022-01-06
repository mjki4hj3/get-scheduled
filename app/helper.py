#Helper Functions
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


def input_request(message): 
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
        
    return max_duration/60