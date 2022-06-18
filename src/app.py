import os
import tweepy
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# load the .env file variables
load_dotenv()

# your app code here
consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
bearer_token = os.environ.get('BEARER_TOKEN')

client = tweepy.Client(bearer_token, consumer_key, consumer_secret, return_type = requests.Response, wait_on_rate_limit = True)

# make a query: search tweets that have the hashtag #100daysofcode and the word python or pandas, from the last 7 days (search_recent_tweets)
query = '#100daysofcode (pandas OR python) -is:retweet'
resp = client.search_recent_tweets(query = query, tweet_fields=['author_id','created_at','lang'], max_results = 100) 
print(resp.text)

# convert to pandas dataframe
resp_dict = resp.json()
resp_data = resp_dict['data']
df = pd.json_normalize(resp_data)
df.head()

# save to csv
df.to_csv("coding-tweets.csv")

# define function word_in_text()
def word_in_text(word, tweet):
    tweet.lower()
    word.lower()
    if word in tweet:
        return True
    else:
        return False

# iterate through dataframe rows counting the number of tweets in which pandas and python are mentioned, using your word_in_text() function
count_1 = 0
count_2 = 0

for index, row in df.iterrows():
    if word_in_text('python', row['text']):
        count_1 += 1
    if word_in_text('pandas', row['text']):
        count_2 += 1

print(count_1)
print(count_2)

# visualize data
sns.set_theme(style="whitegrid", palette="pastel")
lista = [count_1, count_2]
cd = ['pandas', 'python']
ax = sns.barplot(cd, lista)
ax.set(xlabel = 'words', ylabel = 'count')
plt.show()