import tweepy
import pandas as pd
import random
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Twitter API v2
client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

# CSV’yi oku
df = pd.read_csv("tarih_olaylari.csv")

# Bugünün tarihi
bugun = datetime.now()
gun = bugun.day
ay = bugun.month

# Bugüne ait olaylar
bugunun_olaylari = df[(df['gun'] == gun) & (df['ay'] == ay)]

if bugunun_olaylari.empty:
    print("Bugün için olay yok.")
    exit()

# SADECE 12:00, 16:00 ve 20:00’de çalışsın
izin_verilen_saatler = {12, 16, 20}

if bugun.hour not in izin_verilen_saatler:
    print(f"Saat {bugun.hour:02d}:00 → Sadece 12/16/20 dışı, tweet atılmadı.")
    exit()

# Aynı saatte birden fazla tweet atmaması için (ilk 5 dakika içinde çalışsın)
if bugun.minute >= 6:
    print(f"Saat {bugun.hour:02d}:{bugun.minute:02d} → Bu saatin ilk 5 dakikası geçti, bir sonraki saati bekliyor.")
    exit()

# Rastgele bir olay seç ve tweet oluştur
secilen = bugunun_olaylari.sample(1).iloc[0]
ay_adi = str(secilen['ay']).strip()

tweet = f"25 {ay_adi} {secilen['yil']}\n\n{secilen['olay']}\n\n#Tarih #Bugün"

try:
    client.create_tweet(text=tweet)
    print("Tweet başarıyla atıldı! Saat:", bugun.strftime("%H:%M"))
    print(tweet)
except Exception as e:
    print("Hata:", e)
