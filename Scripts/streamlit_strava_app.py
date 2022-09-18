import pandas as pd
import streamlit as st

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(df)

df.drop(columns={'start_date','workout_type','distance','moving_time','elapsed_time','average_speed'},inplace=True)

def race_count(run_category):
    if run_category == 'Race':
        return 1
    else:
        return 0    

df['race_counter'] = df.run_category.apply(race_count)        

analysis = df[df['year']==2022]
distance = analysis.groupby('month').agg({'distance_km':'sum'}).reset_index()
elevation = analysis.groupby('month').agg({'total_elevation_gain':'sum'}).reset_index()
kudo = analysis.groupby('month').agg({'kudos_count':'sum'}).reset_index()
summary = df.groupby('year').agg({'distance_km':'sum','total_elevation_gain':'sum','race_counter':'sum'}).reset_index()

st.write("""# Strava Data Analysis
  YTD 2022 Recap  
  Created by *Ben Bergan*""")

st.caption ('This chart displays the km''s ran per month in 2022')
st.bar_chart(distance, x='month', y='distance_km')
st.caption ('This chart displays total elevation gain per month in 2022')
st.line_chart(elevation, x='month',y='total_elevation_gain')
st.caption ('This chart displays strava wanker count per month in 2022')
st.line_chart(kudo, x='month',y='kudos_count')
st.caption ('The table below compares the year on year performance')
st.table(summary)

