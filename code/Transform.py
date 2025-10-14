import pandas as pd
import streamlit as st
from Api_calls import filename
import time
import re

# Finally I want to save the data to a csv file
# but first I need to remove the emojis

def clean_data(df):

    # Many text have emojis, so they will be removed
    df['title'] = df['title'].str.encode('ascii', 'ignore').str.decode('ascii')

    # Remove rows where 'title' has less than 2 words
    df = df[df['title'].str.split().str.len() > 2]

#----------------------------------------------
    # # Many text have emojis, so they will be removed
    df['selftext'] = df['selftext'].str.encode('ascii', 'ignore').str.decode('ascii')

    # # # Remove rows where 'selftext' is blank
    # df = df[df['selftext'].notna()]


    # Remove rows where 'selftext' contains a URL
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    df = df[~df['selftext'].str.contains(url_pattern, na=False)]
 

    # Remove rows where 'selftext' has less than 2 words
    df = df[df['selftext'].str.split().str.len() >= 2]

    # need make the epoch time into datetime and to organize the datetime 
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')

    return df


#----------------------------------------------
# combine both dataframes into one
df = pd.read_csv(filename)

df_clean = clean_data(df)

filedate = time.strftime("excel_files/Sims4_new_%Y-%m-%d.csv")
df_clean.to_csv(filedate, index=False)

#st.dataframe(df_clean)



# @st.cache_data
# def convert_df(df):
#     return df.to_csv().encode('utf-8')

# csv = convert_df(df)
# st.download_button(
#     "Download CSV",
#     csv,
#     "sims4_subreddit_data.csv",
#     "text/csv",
#     key='download-csv'
# )






#----------------------------------------------
# Importing into a streamlit so I
# can view the data better