#Helper Functions
def round_to_minimum_duration(value, study_block):
    if value < study_block:
        value = study_block
    else:
        value = 1
    return value

# function to split oversized topics into defined study periods
def splitting_function(index, sum, input_value, df):
    
    # scheduling the oversized topic with remaining space in current study period
    space = input_value - (sum - df.loc[index,'Duration (Hours)'])
    
    excess = df.at[index, 'Duration (Hours)'] - space
    df.at[index, 'Duration (Hours)'] = space # scheduling the oversized topic with remainder time
    
    # splitting the remainder of the oversized topic 
    
    slot = 0.01
    # splitting oversized into as many study slots equal to defined studyperiod 
    while excess > input_value:
        df.loc[index + slot] = df.loc[index]
        df.loc[(index + slot), 'Duration (Hours)'] = input_value
        excess = excess - input_value
        slot+= 0.01

    # scheduling the remainder of the oversized topic
    df.loc[index + slot] = df.loc[index]
    df.loc[(index + slot), 'Duration (Hours)'] = excess

    return df


def input_request(message): 
    while True:
        try:
            input_value = float(input(message))
            if input_value > 0:
                break
            elif input_value == 0:
                print("Please enter a non-zero study duration")
                continue
            else:
                print("Please enter a non-negative study duration")
                continue
        except:
            print("Please enter a number")
            continue
        
    return input_value/60