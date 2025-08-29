import numpy as np

def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
         x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
         x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x

def medal_telly(df):
    medal_telly = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_telly = medal_telly.groupby("region").sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending = False).reset_index()
    medal_telly['total'] = medal_telly['Gold'] + medal_telly['Silver'] + medal_telly['Bronze']

    medal_telly['Gold'] = medal_telly['Gold'].astype('int')
    medal_telly['Silver'] = medal_telly['Silver'].astype('int')
    medal_telly['Bronze'] = medal_telly['Bronze'].astype('int')
    medal_telly['total'] = medal_telly['total'].astype('int')

    return medal_telly

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country


def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Editions', 'count': col}, inplace=True)
    return nations_over_time



def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how = 'left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'Name' : 'Name' , 'count' : 'Medals'} , inplace = True)
    return x


def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby("Year").count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')

    return pt


def most_successful_county_wise_athletes(df,country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='Name',right_on='Name',how = 'left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns={'Name' : 'Name' , 'count' : 'Medals'} , inplace = True)
    return x




def medal_trend_for_country(df, selected_country):
    # Drop duplicates to avoid overcounting team medals
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = temp_df[temp_df['region'] == selected_country]

    # Group by Year and sum medals
    medal_tally = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().reset_index()

    # Reshape from wide → long format for plotting
    medal_tally = medal_tally.melt(
        id_vars='Year',
        value_vars=['Gold', 'Silver', 'Bronze'],
        var_name='Medal',
        value_name='Count'
    )
    return medal_tally




### Athletes wise Analysis

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna("No Medal", inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] ==  sport]
        return temp_df
    else:
        return  athlete_df


def men_vs_female(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)

    return final


#  ********* Sport wise Analysis **********
def top_sports_by_athletes(df):
    return df.groupby('Sport')['Name'].nunique().sort_values(ascending=False).reset_index()


def sport_medal_trend(df,sport):
    medal_df = df.dropna(subset = ['Medal'])
    medal_df = medal_df.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Event','Medal'])
    sport_df = medal_df[medal_df['Sport'] == sport]
    trend = sport_df.groupby('Year').count()['Medal'].reset_index()

    return trend


def sport_medal_type_trend(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = temp_df[temp_df['Sport'] == sport]
    medal_df = temp_df.groupby(['Year','Medal']).count()['Name'].reset_index()
    return medal_df


def top_countries_per_sport(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df.groupby('region').count()['Medal'].reset_index().sort_values('Medal',ascending=False).head(10)
    return x


def sport_event_trend(df,sport):
    temp_df = df.drop_duplicates(['Year','Sport','Event'])
    temp_df = temp_df[temp_df['Sport'] == sport]
    x = temp_df.groupby('Year').count()['Event'].reset_index()
    return x