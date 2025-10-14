import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import pandas as pd
import Api_calls
from PIL import Image


# I need a plot that will show the difference between positive, neutral, and negative sentiment
# Loading data
sentiment_data = pd.read_csv('excel_files/merged_sentiment.csv')
sentiment_data['count'] = 1

# barplot
# figure, series1 = plt.subplots()
# bar = sns.barplot(data=sentiment_data, x="sentence_sentiment", y='max_confidence_score', hue= "sentence_sentiment", estimator="sum").set_title("Sentiment Analysis of Sims 4 Subreddit")
# from PIL import Image

#----------------------------------------------
# Image mask 
smile = np.array(Image.open("Images/smiling-face.png"))
meh = np.array(Image.open("Images/neutral-face.png"))
frown = np.array(Image.open("Images/frowning-face.png"))


# def transform_format(val):
#     if val.all() == 0:
#         return 255
#     else:
#         return val

# # pos
# transformed_p = np.ndarray((smile.shape[0], smile.shape[1]), np.int32)

# for i in range(len(smile)):
#     transformed_p[i] = list(map(transform_format, smile[i]))
# print(transformed_p)

# #neu
# transformed_nu = np.ndarray((meh.shape[0], meh.shape[1]), np.int32)

# for i in range(len(meh)):
#     transformed_nu[i] = list(map(transform_format, meh[i]))
# print(transformed_nu)

# #neg
# transformed_ng = np.ndarray((frown.shape[0], frown.shape[1]), np.int32)

# for i in range(len(frown)):
#     transformed_ng[i] = list(map(transform_format, frown[i]))
# print(transformed_ng)
#----------------------------------------------
# I need a word cloud that will show the most common words in the selftext

# Removing these words from wordcloud
STOPWORDS = ["the", "to", "it", "is", "and", "who", "what", "my", "I", "when", "this", "sim", "that",
"for", "a", "but", "with", "by", "of", "me", "her", "just", "are", "you", "so", "in",
"as", "on", "get", "he", "she", "do", "have", "all", "or", "them", "was", "they", "can", "from", 
"up", "be", "if", "at", "has", "its", "amp", "there", "had", "then", "an", "did", "how", "where",
"too", "him", "sims", "hi", "I'm","because"]

my_dpi = 100

# positive word cloud

pos_words = sentiment_data[sentiment_data['Sentiment_Label'] == 'Positive']
pos_cloud = WordCloud(width = 800/my_dpi, height = 800/my_dpi, background_color='white', stopwords=STOPWORDS, mask = smile, contour_width=2, contour_color='black').generate(' '.join(pos_words['selftext'])).to_file("Images/smile.png")

print(pos_cloud)

figure2 = plt.figure(figsize = (10,2))
plt.title('Positive Sentiment')
plt.imshow(pos_cloud, interpolation="bilinear")
plt.axis("off")


# negative word cloud

neg_words = sentiment_data[sentiment_data['Sentiment_Label'] == 'Negative']
neg_cloud = WordCloud(width = 400/my_dpi, height = 800/my_dpi, background_color='white', stopwords=STOPWORDS, mask = frown, contour_width=2, contour_color='black').generate(' '.join(neg_words['selftext'])).to_file("Images/frown.png")


figure3 = plt.figure(figsize = (10,2))
plt.title('Negative Sentiment')
plt.imshow(neg_cloud, interpolation="bilinear")
plt.axis("off")


# neutral word cloud

neutral_words = sentiment_data[sentiment_data['Sentiment_Label'] == 'Neutral']
neutral_cloud = WordCloud(width = 800/my_dpi, height = 800/my_dpi, background_color='white', stopwords=STOPWORDS, mask = meh, contour_width=2, contour_color='black').generate(' '.join(neutral_words['selftext'])).to_file("Images/meh.png")


figure4 = plt.figure(figsize = (10,2))
plt.title('Nuetral Sentiment')
plt.imshow(neutral_cloud, interpolation="bilinear")
plt.axis("off")

#---------------------------------------------------------

# 100% stacked bar plot

# Finding the 11 most utilized words without stop/filler words that are
# commonly found in each sentiment



# replacing text of pos, neg, and neu with number representation

to_int = {'Positive': 1, 'Neutral': 2, 'Negative': 3}



#----------------------------------------------

# I want to have a sidebar that shows plots
st.sidebar.title("Plots")
# #barplot
with st.sidebar:
#     # Display the plot in Streamlit
#     st.pyplot(figure)
#wordplots
    st.pyplot(figure2)
    st.pyplot(figure3)
    st.pyplot(figure4)

# I want a main section that shows and allows for the dataframe to be downloaded
st.title("Sims 4 Subreddit Data")
st.dataframe(sentiment_data)
csv = sentiment_data.to_csv(index=False).encode('utf-8')
st.download_button(label="Download CSV file", data=csv, file_name='sims4_sentiment_data.csv', mime='text/csv',
)