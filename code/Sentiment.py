from pathlib import  Path
import pandas as pd
from Transform import df_clean
from Transform import filedate
import time
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm



sia = SentimentIntensityAnalyzer()

Sims4_df = df_clean

# getting the sentiments based on each comment 
sentiments = []
for index, row in Sims4_df.iterrows():

    sentiment_score = sia.polarity_scores(row['selftext'])
    compound = sentiment_score['compound']


    if compound >= 0.05:
        sentiment = 'Positive'
    elif compound <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    sentiments.append({
    'Positive': sentiment_score['neg'],
    'Negative': sentiment_score['pos'],
    'Neutral': sentiment_score['neu'],
    'Compound': sentiment_score['compound'],
    'Sentiment_Label': sentiment

    })

# save to cache, return dataframe and save it to a csv file

cwd = Path(__file__).parent
script_dir = cwd.parent.parent.resolve() / "Sims4_Sentiment-Analysis"/"excel_files"

sentiment_df = pd.DataFrame(sentiments)
s_file = sentiment_df.to_csv(script_dir/"Sims_sentiment.csv", index=False)

# Concat the sims_new file and the sims sentiment.csv file
concating = pd.concat(map(pd.read_csv, [filedate, script_dir/"Sims_sentiment.csv"]), axis=1)

file = (script_dir/time.strftime("Sims4_merged_%Y-%m-%d.csv"))
concating.to_csv(file, index=False)

