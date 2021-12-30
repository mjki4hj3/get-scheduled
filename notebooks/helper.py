def round_to_minimum_duration(df):
    df.loc[df['Duration'] < 0.5, ['Duration']] = 0.5
    return df