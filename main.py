import tweepy
import pandas as pd
import random
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

df = pd.read_csv("tarih_olaylari.csv")

bugun = datetime.now()
gun = bugun.day
ay = bugun.month

ay_isimleri = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
               "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

bugun_olaylari = df[(df['gun'] == gun) & (df['ay'] == ay)]

if not bugun_olaylari.empty and random.random() < 0.8:
    secilen = bugun_olaylari.sample(1).iloc[0]
else:
    secilen = df.sample(1).iloc[0]

ay_no = int(secilen['ay'])
tweet = f"25 Kasım {ay_isimleri[ay_no]} {secilen['yil']}\n\n{secilen['olay']}\n\n#Tarih #Bugün"

try:
    client.create_tweet(text=tweet)
    print("Tweet başarıyla atıldı!")
    print(tweet)
except Exception as e:
    print("Hata:", e)
