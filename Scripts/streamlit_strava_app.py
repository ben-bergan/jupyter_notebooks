from sre_constants import ANY_ALL
import pandas as pd
import streamlit as st

df = pd.read_csv('..//Output//strava_run_data.csv')
df.drop(columns={'start_date','workout_type','distance','moving_time','elapsed_time','average_speed'},inplace=True)

def race_count(run_category):
    if run_category == 'Race':
        return 1
    else:
        return 0    

df['race_counter'] = df.run_category.apply(race_count)      

st.write("""# Strava Data  
  yearly data analysis
  Created by *Ben Bergan*""")

year_select = df.year.unique().tolist()

option = st.selectbox('Select the year:',year_select)

analysis = df[df['year']==option]

distance = analysis.groupby('month').agg({'distance_km':'sum'}).reset_index()
elevation = analysis.groupby('month').agg({'total_elevation_gain':'sum'}).reset_index()
summary = df.groupby('year').agg({'distance_km':'sum','total_elevation_gain':'sum','race_counter':'sum'}).reset_index()
summary = summary.sort_values(by='year', ascending=False)
summary.rename(columns={'distance_km':'Distance','total_elevation_gain':'Elevation Gain','race_counter':'Races'},inplace=True)
year_summary = df[(df['year']==option) & (df['race_counter']==1)]
year_summary = year_summary[['name','start_date_converted','distance_km','moving_time_converted','pr_count']]
year_summary.rename(columns={'name':'Race Name','start_date_converted':'Race Date','distance_km':'Distance','moving_time_converted':'Moving Time','pr_count':'PB Count'},inplace=True)

st.caption ('This chart displays the km''s ran per month in the selected year')
st.bar_chart(distance, x='month', y='distance_km')
st.caption ('This chart displays total elevation gain per month in the selected year')
st.line_chart(elevation, x='month',y='total_elevation_gain')
st.caption ('The table below lists all races in the selected year')
st.table(year_summary)
st.caption ('The table below compares the year on year performance')
st.table(summary)

