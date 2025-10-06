import os
import feedparser
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup
import lxml

engine = create_engine('mysql+mysqldb://username:password@localhost:3306/lottery', echo=False)

# URL OF RSS FEED
feed_url = "https://feeds.feedblitz.com/pennsylvanialottery-winningnumbers-dailynumbermid-dayandevening"
feed = feedparser.parse(feed_url)
# r = requests.get(feed_url)
# soup = BeautifulSoup(r.content, features="lxml")

data = []

# GET ALL RECORDS AVAILABLE
# for e in range(len(feed.entries)):

# GET MOST RECENT WINNING NUMBERS / INCREMENTS
for e in range(2):
    type_date = feed.entries[e].title_detail.value
    winning_numbers = feed.entries[e].summary_detail.value
    data.append((type_date, winning_numbers))

df = pd.DataFrame(data)
df.columns = ['type_date', 'winning_numbers']
df['date'] = pd.to_datetime(df['type_date'].str[-10:])
df['numbers'] = df['winning_numbers'].str[17:23:2]
df['n1'] = df['winning_numbers'].str[17]
df['n2'] = df['winning_numbers'].str[19]
df['n3'] = df['winning_numbers'].str[21]
df['wb'] = df['winning_numbers'].str[28:29]
# os.remove('daily.csv')
# df.to_csv('daily.csv', index_label='index_id')
df.to_sql(name='daily_pick3', con=engine, if_exists='append', index=False)
# print(df)
