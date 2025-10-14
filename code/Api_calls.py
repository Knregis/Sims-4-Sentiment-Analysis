import pandas as pd
import streamlit as st
import requests
import time
from time import sleep
import config



# starting off by gaining access to the reddit API

auth = requests.auth.HTTPBasicAuth(config.Client_ID, config.Secret_Key)

data = {
    'grant_type': 'password',
    'username': config.auth1,
    'password': config.auth2
}

headers = {
    'User-Agent': 'script/project3:v1.0'
    }

    #----------------------------------------------

    # Now I am getting token access to the API


TOKEN_ACCESS = 'https://www.reddit.com/api/v1/access_token'

res = requests.post(TOKEN_ACCESS, auth=auth, data=data, headers=headers)

if res.status_code == 200:
    TOKEN = res.json()['access_token']

print(res.status_code)
print(res.text)

headers['Authorization'] = f'bearer {TOKEN}'


        #----------------------------------------------

        # In the function I want to 
        # make getting posts easier
        # by not hardcoding the parameters
        # and by combining the dataframes into one

query = ' title:("lov*" OR "lik*" OR "best" OR "I love this game" OR "This game is the best" OR "This game is good" OR "I like this game" OR "good" OR "amazing") \
OR title:("this game is" OR "Unpopular Opinion" OR "regret" OR "I wish" OR "This game needs") \
OR title:("I hate" OR "This game is the worst" OR "This game is ba*" OR "I hate this game" OR "ba*" OR "There is a bug" OR "bug" OR "This bug" OR "error" OR "worst") \
OR selftext:("lov*" OR "lik*") OR selftext:("I hate" OR "the worst" OR "I regret" OR "difficul*") '

endpoint = 'https://oauth.reddit.com/r/Sims4/search/'


def get_posts(endpoint, sort, after=None, limit=100):
    for calls in range(100):

        params = {
                'q': query,
                'type': 'posts',
                'restrict_sr': 'on',
                'sort': sort,
                't': 'all',
                'limit': limit,
                'after': after
            }

        all_posts = []  

    #----------------------------------------------
        # part about pagination that I will use to get more posts
        
        while True:

            params['after'] = after

            response = requests.get(endpoint, headers=headers, params=params, allow_redirects=False)
            data_json = response.json()

            if 'data' not in data_json or 'children' not in data_json['data']:
                break

            posts = data_json['data']['children']
            all_posts.extend(posts)

            after = data_json['data'].get('after')

            if not after or len(all_posts) >= 1000:
                break
            
            time.sleep(2)

        return all_posts
    
    # print("Reddit API call complete")
    # sleep(60)
    # exit()

#----------------------------------------------



# Combine all posts into one list 
top_posts = get_posts(endpoint, 'top')
hot_posts = get_posts(endpoint, 'hot')
new_posts = get_posts(endpoint, 'new')

combine = top_posts + hot_posts + new_posts

#----------------------------------------------

# Now I want to place data into a pandas dataframe
# and combinine the dataframes into one


df = pd.DataFrame([{
    'title': post['data']['title'],
    'selftext': post['data']['selftext'],
    'upvote_ratio': post['data']['upvote_ratio'],
    'ups': post['data']['ups'],
    'downs': post['data']['downs'],
    'score': post['data']['score'],
    'date': post['data']['created_utc']
} for post in combine])


#----------------------------------------------
# Importing into a streamlit so I
# can view the data better

#st.title("Sims 4 Subreddit Data")

filename = time.strftime("excel_files/Sims4_data_%Y-%m-%d.csv")
df = df.to_csv(filename, index=False)


