import numpy as np

def fetch_medal_tally(summer, year, country):

    medal_df = summer.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]

    if flag == 1:
        x = temp_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()

    else:
        x = temp_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    return x


def country_year_list(summer):
    # to find the years in which olympic was played
    years = summer['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    # to find out all the unique countries that participated in summer olympics
    country = np.unique(summer['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country

def participating_nations_over_time(summer):
    # Drop duplicates based on 'Year' and 'region'
    nations_over_time = summer.drop_duplicates(subset=['Year', 'region'])

    # Count the number of unique 'region' entries per 'Year'
    nations_over_time = nations_over_time.groupby('Year')['region'].nunique().reset_index()

    nations_over_time.rename(columns={'Year': 'Edition', 'region': 'No of Countries'}, inplace=True)
    return nations_over_time

def event_over_time(summer):
    event_over_time = summer.drop_duplicates(subset=['Event', 'Year'])
    event_over_time = event_over_time.groupby('Year')['Event'].nunique().reset_index()
    return event_over_time

def athlete_participation_over_time(summer):
    athlete_over_time = summer.drop_duplicates(subset=['Name', 'Year'])
    athlete_over_time = athlete_over_time.groupby('Year')['Name'].nunique().reset_index()
    athlete_over_time.rename(columns={'Name': 'No of Athletes'}, inplace=True)
    return athlete_over_time


def most_successful(summer, sport):
    temp_df = summer.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(summer, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def yearwise_medal_tally_of_countries(summer, country):
    temp_df = summer.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year')['Medal'].count().reset_index()
    return final_df

def country_wise_heatmap(summer, country):
    temp_df = summer.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def most_successful_athlete_country_wise(summer, country):
    # We don't want the athletes who haven't won any medal
    temp_df = summer.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == str(country)]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(summer, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')

    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x
