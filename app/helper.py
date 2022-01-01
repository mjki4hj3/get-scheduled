#Helper Functions
def round_to_minimum_duration(value):
    if value < 0.5:
        value = 0.5
    else:
        value = 1
    return value

# function to split oversized topics into defined study periods
def splitting_function(index, sum, study_period, df):
    # scheduling the oversized topic with remaining space in current study period
    space = study_period - (sum - df.loc[index,'Duration (Hours)'])
    df.at[index, 'Duration (Hours)'] = space # scheduling the oversized topic with remainder time
    
    # splitting the remainder of the oversized topic 
    excess = df.at[index, 'Duration (Hours)'] - space
    slot = 0.01
    # splitting oversized into as many study slots equal to defined studyperiod 
    while excess > study_period:
        df.loc[index + slot] = df.loc[index]
        df.loc[(index + slot), 'Duration (Hours)'] = study_period
        excess = excess - study_period
        slot+= 0.01

    # scheduling the remainder of the oversized topic
    df.loc[index + slot] = df.loc[index]
    df.loc[(index + slot), 'Duration (Hours)'] = excess

    return df
    