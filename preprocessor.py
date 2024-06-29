import pandas as pd



def preprocess(df, region_df):

    # filtering for summer olympics
    summer = df[df['Season'] == 'Summer']
    # merge with region_df
    summer = summer.merge(region_df, on='NOC', how='left')
    # dropping duplicates
    summer.drop_duplicates(inplace=True)
    # one hot encoding medals
    summer = pd.concat([summer, pd.get_dummies(summer['Medal'])], axis=1)
    return summer
