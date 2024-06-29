import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

summer = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Olympic_flag.svg/512px-Olympic_flag.svg.png")

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(summer)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s Overall Performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s Overall Performance in year " + str(selected_year))
    medal_tally = helper.fetch_medal_tally(summer, selected_year, selected_country)
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = summer['Year'].unique().shape[0]-1
    cities = summer['City'].unique().shape[0]
    sports = summer['Sport'].unique().shape[0]
    events = summer['Event'].unique().shape[0]
    athletes = summer['Name'].unique().shape[0]
    nations = summer['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    nations_over_time = helper.participating_nations_over_time(summer)
    fig = px.line(nations_over_time, x="Edition", y="No of Countries")
    st.title("Participating Nations over the Years")
    st.plotly_chart(fig)

    event_over_time = helper.event_over_time(summer)
    fig = px.line(event_over_time, x='Year', y='Event')
    st.title("Events over the Years")
    st.plotly_chart(fig)

    athlete_over_time = helper.athlete_participation_over_time(summer)
    fig = px.line(athlete_over_time, x = 'Year', y='No of Athletes')
    st.title("Athlete Participation over the Years")
    st.plotly_chart(fig)

    st.title("No. of Events in different Sports over Time")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = summer.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    # st.title("Most Successful Athletes")
    # x = helper.most_successful(summer, 'Overall')
    # st.table(x)


if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = summer['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select Country', country_list)

    country_df = helper.yearwise_medal_tally_of_countries(summer, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the Years")
    st.plotly_chart(fig)

    pt = helper.country_wise_heatmap(summer, selected_country)
    st.title(selected_country + " Performance in different Sports")
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    # st.title("Top 10 athletes of " + selected_country)
    # top10_df = helper.most_successful_athlete_country_wise(summer, selected_country)
    # st.table(top10_df)


if user_menu == 'Athlete wise Analysis':
    athlete_df = summer.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    st.title("Age Wise Distribution of Athletes")

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)

    st.plotly_chart(fig)
