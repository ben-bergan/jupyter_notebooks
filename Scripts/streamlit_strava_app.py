from sre_constants import ANY_ALL
import pandas as pd
import streamlit as st
from pathlib import Path
import numpy as np

strava_run_data = Path(__file__).parents[0] / 'strava_run_data.csv'

df = pd.read_csv(strava_run_data)

df.drop(columns={'achievement_count','comment_count','kudos_count'},inplace=True)

def race_count(run_category):
    if run_category == 'Race':
        return 1
    else:
        return 0    

df['race_counter'] = df.run_category.apply(race_count)      

st.write("""# Strava Data Analysis 
  Version 1.1
  Created by Ben Bergan""")

year_select = df.year.unique().tolist()

option = st.selectbox('Select the year:',year_select)
delta = option-1

analysis = df[df['year']==option]
analysis_prior = df[df['year']==delta]

distance = analysis.groupby('start_date_month').agg({'distance_km':'sum'}).reset_index()
distance_year = analysis.groupby('year').agg({'distance_km':'sum'}).reset_index(drop=True)
distance_year = np.array(distance_year)[0]
distance_prior_year = analysis_prior.groupby('year').agg({'distance_km':'sum'}).reset_index(drop=True)
distance_prior_year = np.array(distance_prior_year)[0]
elevation = analysis.groupby('start_date_month').agg({'total_elevation_gain':'sum'}).reset_index()
elevation_year = analysis.groupby('year').agg({'total_elevation_gain':'sum'}).reset_index(drop=True)
elevation_year = np.array(elevation_year)[0]
elevation_prior_year = analysis_prior.groupby('year').agg({'total_elevation_gain':'sum'}).reset_index(drop=True)
elevation_prior_year = np.array(elevation_prior_year)[0]

summary = df.groupby('year').agg({'distance_km':'sum','total_elevation_gain':'sum','race_counter':'sum'}).reset_index()
summary = summary.sort_values(by='year', ascending=False)
summary.rename(columns={'distance_km':'Distance','total_elevation_gain':'Elevation Gain','race_counter':'Races'},inplace=True)
year_summary = df[(df['year']==option) & (df['race_counter']==1)]
year_summary = year_summary[['name','start_date_converted','distance_km','run_elapsed_time','average_cadence','average_heartrate']]
year_summary.rename(columns={'name':'Race Name','start_date_converted':'Race Date','distance_km':'Distance','run_elapsed_time':'Race Time','average_cadence':'Average Cadence','average_heartrate':'Average Heartrate'},inplace=True)

col1, col2 = st.columns(2)
col1.metric('Yearly Distance - Compared to Prior Year', distance_year, round(float(distance_year - distance_prior_year),2))
col2.metric('Yearly Elevation Gain - Compared to Prior Year', elevation_year, round(float(elevation_year - elevation_prior_year),2))

st.caption ('This chart displays the km''s ran per month in the selected year')
st.bar_chart(distance, x='start_date_month', y='distance_km')
st.caption ('This chart displays total elevation gain per month in the selected year')
st.bar_chart(elevation, x='start_date_month',y='total_elevation_gain')
st.caption ('The table below lists all races in the selected year')
st.table(year_summary)
st.caption ('The table below compares the year on year performance')
st.table(summary)
