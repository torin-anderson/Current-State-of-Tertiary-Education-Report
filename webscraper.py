# %%
import pandas as pd
import praw
import re
from urllib.request import urlopen
import json
import time
from datetime import datetime
from gensim. corpora import Dictionary
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from gensim.models import Phrases
import numpy as np

# %%
#information to search reddit
CLIENT_ID = '1O2xUimjO3SVLmtJoNtfLg'
CLIENT_SECRET = '0suqeoN8nXIwFc5LZF4EGhTwZ5kqTQ'
USER_AGENT = 'Icy-Dust5622'

#searches reddit for subreddit
reddit= praw.Reddit(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        user_agent = USER_AGENT)

urls = []
#finds threads off of subreddit if they are from reddit and not another website
for thread in reddit.subreddit('college').hot(limit=5000):
    url = thread.url
    if re.search(r'www.reddit.com/r/', url):
        urls.append(url)
        print("From subreddit: ", url)

with open('college.json', 'w+') as fp: #creates file
    for url in urls:
        #tries to search for url json, but if it reports too many requests waits 4 more seconds
        while True:
            try:
                response = urlopen(url+'.json') #makes it so that json url is opened
                json_str = response.read()
                jobj = json.loads(json_str)
                if (len(jobj) > 0):
                    jstr = json.dumps(jobj)
                    print("Into json file ", jstr)
                    fp.write(jstr+'\n')
                time.sleep(4) #so too many requests don't happen
                break
            except:
                time.sleep(4) 

# %%
urls = []
#finds threads off of subreddit if they are from reddit and not another website
for thread in reddit.subreddit('Sat').hot(limit=5000):
    url = thread.url
    if re.search(r'www.reddit.com/r/', url):
        urls.append(url)
        print("From subreddit: ", url)

with open('Sat.json', 'w+') as fp: #creates file
    for url in urls:
        #tries to search for url json, but if it reports too many requests waits 4 more seconds
        while True:
            try:
                response = urlopen(url+'.json') #makes it so that json url is opened
                json_str = response.read()
                jobj = json.loads(json_str)
                if (len(jobj) > 0):
                    jstr = json.dumps(jobj)
                    print("Into json file ", jstr)
                    fp.write(jstr+'\n')
                time.sleep(4) #so too many requests don't happen
                break
            except:
                time.sleep(4) 

# %%
urls = []
#finds threads off of subreddit if they are from reddit and not another website
for thread in reddit.subreddit('ApplyingToCollege').hot(limit=5000):
    url = thread.url
    if re.search(r'www.reddit.com/r/', url):
        urls.append(url)
        print("From subreddit: ", url)

with open('ApplyingToCollege.json', 'w+') as fp: #creates file
    for url in urls:
        #tries to search for url json, but if it reports too many requests waits 4 more seconds
        while True:
            try:
                response = urlopen(url+'.json') #makes it so that json url is opened
                json_str = response.read()
                jobj = json.loads(json_str)
                if (len(jobj) > 0):
                    jstr = json.dumps(jobj)
                    print("Into json file ", jstr)
                    fp.write(jstr+'\n')
                time.sleep(4) #so too many requests don't happen
                break
            except:
                time.sleep(4) 

# %%
titles = ['Sat', 'college', 'ApplyingToCollege']

#function that searches throuhgh json file and saves the author, created time, and the text
def get_post(jobj):
    dataobj = jobj[0]['data']['children'][0]['data']
    txt = dataobj['selftext']
    author = dataobj['name']
    time = dataobj['created_utc']
    return {
        'author': author,
        'created_utc' : time,
        'text' : txt
    }

#function that searches through all of the comments from the original json file and saves author, created time, and text
def get_comment(jobj):
    comments = []
    for comment in jobj[1]['data']['children']:
        if 'author' in comment['data'] and 'created_utc' in comment['data'] and 'body' in comment['data']:
            cobj = {
                'author': comment['data']['name'],
                'created_utc': comment['data']['created_utc'],
                'text': comment['data']['body']
            }
        comments.append(cobj)
    return comments

#function that finds vector representation for each token
def get_vector(bow,dct):
    vector_len = len(dct.token2id)
    vector = np.zeros(vector_len)
    for tk in bow:
        vector[tk[0]] = tk[1]
    vector = vector/sum(vector)
    return vector



for title in titles:
    with open(title+ '.json', 'r+') as fp:
        lines = fp.readlines()


    #iterates through all of the scraped posts and returns all of the posts along with comments
    all_posts = []
    for line in lines:
        data_obj = json.loads(line)
        dobj = get_post(data_obj) #gets original post
        all_posts.append(dobj)
        comments = get_comment(data_obj) #gets comments
        all_posts.extend(comments)

    #creates dataframe from json files searched through
    df = pd.DataFrame(all_posts)
    df['timestamp'] = df['created_utc'].apply(lambda epoch:datetime.fromtimestamp(epoch)) #converts created utc to datetime format
    df = df.sort_values(by='created_utc') #sorts dataframe based on earliest posts first
    df=df.reset_index(drop=True)

    #converts text to tokens, bow, and finds vector representation and cosine similarity
    df['text'] = df['text'].apply(str.lower)
    #remove @s, #s, urls, and rt
    df['tokens'] = df['text'].apply(lambda txt: re.sub(r'@\w+|#\w+|http.+|rt\s', '', txt))
    #tokenizes the words
    df['tokens'] = df['tokens'].apply(word_tokenize)

    #find phrases that have been used 30 or more times
    phraser = Phrases(df['tokens'], min_count=30, delimiter='_')
    df['tokens'] = df['tokens'].apply(lambda tokens:phraser[tokens])

    #gets rid of stop words
    stop_words = set(stopwords.words('english'))
    df['tokens'] = df['tokens'].apply(lambda tokens: [t for t in tokens if t not in stop_words])

    #keeps words tokenized if they are longer than 3 letters
    df['tokens'] = df['tokens'].apply(lambda tokens: [t for t in tokens if len(t) > 3])

    #stems the token words
    stemmer = PorterStemmer()
    df['tokens'] = df['tokens'].apply(lambda tokens: [stemmer.stem(tk) for tk in tokens])

    #gensim dictionary and filters out words that appear less than twenty times
    dct = Dictionary(df['tokens'])
    dct.filter_extremes(no_below=20) 

    #creates bow column from the dictionary and rows with three or more bow
    df['bow'] = df['tokens'].apply(dct.doc2bow)
    df = df.loc[df['bow'].apply(lambda bow: len(bow) >= 3)]

    #creates vector representation for each index in the bag of words
    df['vector'] = df['bow'].apply(lambda bow: get_vector(bow, dct))
    
    df.to_csv(title + '.csv') #df with game period differentiation saved to csv

    