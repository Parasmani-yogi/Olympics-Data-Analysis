import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff




df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)


st.sidebar.title("Olympics Analysis")
st.sidebar.image('logo_image.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis', 'Country wise Analysis','Athlete wise Analysis','Sport wise Analysis')
)


####   ********** Medal Tally *************

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in '+ str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Performance in ' + str(selected_year) + ' Olympics')
    st.table(medal_tally)

    #  Medal Trend for Selected Country
    if selected_country != 'Overall' and selected_year == 'Overall':
        st.subheader(f"{selected_country} Medal Trend Over the Years")
        country_trend = helper.year_wise_medal_tally(df, selected_country)
        fig = px.line(country_trend, x='Year', y='Medal')
        st.plotly_chart(fig)
        st.markdown(
            """
            This plot shows how the selected country’s **Olympic medal count changed over time**.  
            Peaks indicate years of **highest performance**, while dips show years with **fewer medals**.  
            It helps identify **trends and patterns** in the country’s overall Olympic success.
            """
        )





    # Top Sports for Selected Country
    if selected_country != 'Overall' and selected_year == 'Overall':
        st.subheader(f"{selected_country} Top Sports by Medals")

        temp_df = df.drop_duplicates(
            subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
        )

        temp_df = temp_df[temp_df['region'] == selected_country].dropna(subset=['Medal'])

        sport_medals = (
            temp_df.groupby('Sport')['Medal']
            .count()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )


        fig = px.bar(sport_medals, x='Sport', y='Medal', color='Medal')
        fig.update_layout(
            xaxis_tickangle=90,
            yaxis_title="Number of Medals",
            xaxis_title="Sport"
        )
        st.plotly_chart(fig)

        st.markdown(
            """
            This plot shows the **top 10 sports where the selected country won the most medals**.  
            Team event duplicates have been removed, so the medal counts here are accurate.  
            Taller bars indicate sports in which the country has been most successful historically.
            """
        )





    # Top 10 Countries for Selected Year
    if selected_year != 'Overall' and selected_country == 'Overall':
        top10 = medal_tally.head(10)
        fig = px.bar(
            top10,
            x='region',
            y=['Gold', 'Silver', 'Bronze'],
            title=f"Top 10 Countries - {selected_year}",
            color_discrete_sequence=['gold', 'silver', 'brown']
        )

        fig.update_layout(yaxis_title="Number of Medals",xaxis_title="Country")
        st.plotly_chart(fig)
        st.markdown(
            f"""
            This chart shows the **top 10 countries in {selected_year} Olympics** by total medals.  
            The height of each bar indicates the **total number of medals**, and the colored segments show the **distribution of Gold, Silver, and Bronze**.  
            It highlights which countries dominated the Games that year.
            """
        )

##  ************** Overall Analysis ****************
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    # (shape-1) because more stress was placed on the continuing sequence of four-year Olympiads,
    # and the Games of 1906 did not fit into this. Hence, the IOC currently does not recognise Athens
    # 1906 as Olympic Games, and does not regard any events occurring there (such as the setting of new
    # records or the winning of medals) as official.
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]


    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(editions)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    # Nations over the years
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time,x='Editions',y='region')
    st.title("Participating Nations over the Year")
    st.plotly_chart(fig)
    st.markdown(
        """
        This chart tracks the growth of nations participating in the Olympics.  
        It demonstrates how the Games evolved into a truly global event over time.
        """
    )


    # Events over the years
    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time,x='Editions',y='Event')
    st.title("Events over the Years")
    st.plotly_chart(fig)
    st.markdown(
        """
        This visualization highlights the steady increase in Olympic events.  
        It reflects the expansion of the Games with new sports and competitions.
        """
    )


    # Athletes over the years
    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time,x='Editions',y='Name')
    st.title("Athletes over the Years")
    st.plotly_chart(fig)
    st.markdown(
        """
        This chart highlights the steady rise in the number of athletes participating in the Olympics over time,  
        with occasional dips due to historical events.  
        The overall upward trend reflects the expansion, global reach, and inclusiveness of the Games.
        """
    )

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot =True)
    st.pyplot(fig)
    st.markdown(
        """
        The heatmap compares the number of events per sport across years.  
        It reveals which sports gained more prominence and consistency over time.
        """
    )

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)


    st.title("Most Popular Sports by Number of Events")
    sport_events = df.drop_duplicates(['Year', 'Sport', 'Event']).groupby('Sport')['Event'].count().sort_values(
        ascending=False).head(10).reset_index()
    fig = px.bar(sport_events, x='Sport', y='Event', color='Event')
    fig.update_layout(yaxis_title="Number of Events", xaxis_title="Sport", xaxis_tickangle=90)
    st.plotly_chart(fig)
    st.markdown(
        """
        This bar chart ranks the top sports by number of events.  
        It showcases the disciplines that dominate the Olympic program.
        """
    )

##  ************** Country wise Analysis ***************
if user_menu == 'Country wise Analysis':

    st.sidebar.title('Country wise Analysis')

    # dropna() --> because NaN values present in region column
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal tally over the Years")
    st.plotly_chart(fig)



   # Gold/Silver/Bronze Medal Distribution
    st.title(selected_country + " Gold, Silver, Bronze medal trend over the Years")

    medal_tally = helper.medal_trend_for_country(df, selected_country)

    fig = px.line(
        medal_tally,
        x="Year",
        y="Count",
        color="Medal",
        markers=True,
        color_discrete_map={
            "Gold": "skyblue",
            "Silver": "red",
            "Bronze": "blue"
        }
    )

    st.plotly_chart(fig)

    # Medal Distribution by Type (Gold/Silver/Bronze)
    st.title(f"Medal Distribution of {selected_country}")

    # Drop duplicates first to avoid counting team medals multiple times
    medal_dist = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_dist = medal_dist[medal_dist['region'] == selected_country]['Medal'].value_counts()

    if medal_dist.empty:
        st.warning(f"No medal data available for {selected_country}")
    else:
        fig = px.pie(
            medal_dist,
            names=medal_dist.index,
            values=medal_dist.values,
            title=f"{selected_country} Medal Distribution"
        )
        st.plotly_chart(fig)


    # Heatmap
    st.title(selected_country + " Excels in the following Sports ")
    pt = helper.country_event_heatmap(df, selected_country)

    if pt.empty or pt.shape[0] == 0 or pt.shape[1] == 0:
        st.warning(f"No medal data available for {selected_country}")
    else:
        fig, ax = plt.subplots(figsize=(25, 25))
        sns.heatmap(pt, annot=True)
        st.pyplot(fig)
        st.markdown(
            """
            The heatmap displays **medal counts per sport for each Olympic year**.  
            Higher values highlight the country’s **strongest sports** over time.
            """
        )

    st.title('top 10 Athletes of '+ selected_country)
    top10_df = helper.most_successful_county_wise_athletes(df,selected_country)
    st.table(top10_df)







## ********* Athletes wise Analysis *****************
if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize  = False,width = 1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x_gold = []
    name_gold = []
    x_silver = []
    name_silver = []

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo',
                     'Ice Hockey']


    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x_gold.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name_gold.append(sport)

    fig = ff.create_distplot(x_gold,name_gold,show_hist = False,show_rug = False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age wrt Sports(Gold Medalist)')
    st.plotly_chart(fig)

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x_silver.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name_silver.append(sport)

    fig = ff.create_distplot(x_silver,name_silver,show_hist = False,show_rug = False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age wrt Sports(Silver Medalist)')
    st.plotly_chart(fig)


    ## weight_Vs_height
    st.title("Height Vs Weight")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(data = temp_df, x = 'Weight' , y = 'Height',hue='Medal',style = 'Sex',s=60)

    st.pyplot(fig)


    # Men vs Women Participation
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_female(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'],color_discrete_sequence=['blue', 'red'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


    # Medals by gender
    st.title("Medals by Gender")
    gender_medals = df[df['Medal'].notna()].groupby('Sex').count()['Medal'].reset_index()
    fig = px.pie(gender_medals, names='Sex', values='Medal',
                 title="Medals Share: Men vs Women")
    st.plotly_chart(fig)



# ************* Sport wise Analysis *****************
if user_menu == 'Sport wise Analysis':
    st.title("Sport wise Analysis")

    # top sports by Athletes
    st.subheader("top sports by Number of Athletes")
    sport_df = helper.top_sports_by_athletes(df).head(10)
    fig = px.bar(sport_df,x = 'Sport', y = 'Name' , color = 'Name')
    st.plotly_chart(fig)

    st.title("Performance Analysis by Sport")

    # sport-wise medal trend
    sports_list = sorted(df['Sport'].unique())
    selected_sport = st.selectbox("select a sport",sports_list)
    trend_df = helper.sport_medal_trend(df,selected_sport)
    st.subheader(f'Medal Trend in {selected_sport} over the years')
    fig = px.line(trend_df,x='Year',y='Medal')
    fig.update_layout(xaxis_title = 'Year',yaxis_title = 'Number of Medals',)
    st.plotly_chart(fig)

    # Medal Distribution Over Time by Medal Type
    st.subheader(f"{selected_sport} Medal Type(Gold/Silver/Bronze) Trend")
    medal_type_df = helper.sport_medal_type_trend(df, selected_sport)
    fig = px.line(medal_type_df, x='Year', y='Name', color='Medal', markers=True)
    fig.update_layout(xaxis_title='Year', yaxis_title='Number of Medals')
    st.plotly_chart(fig)

    # Top countries per sport
    st.subheader(f"Top 10 Countries in {selected_sport}")
    top_countries = helper.top_countries_per_sport(df,selected_sport)
    fig = px.bar(top_countries,x='region',y='Medal')
    fig.update_layout(xaxis_title="Country",yaxis_title="Number of Medals")
    st.plotly_chart(fig)

    # Number of Events in sports over years
    st.subheader(f"Number of Events in {selected_sport} Over the Years")
    events = helper.sport_event_trend(df,selected_sport)
    fig = px.line(events,x='Year',y='Event',markers=True)
    fig.update_layout(xaxis_title = 'Year',yaxis_title = 'Number of Events')
    st.plotly_chart(fig)


