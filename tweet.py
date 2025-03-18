import os
import tweepy
import requests
from dotenv import load_dotenv
from random import randint

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def tweet_women_fact(tweepy_client):

   print('fetching women from the MET...')
   r1 = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/search?q=woman")

   parsed = r1.json()

   number = randint(1, 100)

   obj_id = parsed['objectIDs'][number]

   r2 = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}")

   parsed = r2.json()

   if parsed['title'] != '':
       text = f"Title: {parsed['title']}"
   else:
       text = f"Title: Unknown"
   if parsed['artistDisplayName'] != '':
       artist = f"Artist: {parsed['artistDisplayName']}"
   else:
       artist = 'Artist: Unknown'
   if parsed['artistGender'] != '':
       gender = parsed['artistGender']
   else:
       gender = 'Gender: Unknown'

   image = parsed['objectURL']

   tweet_text = f"{text}, {artist}, {gender} {image}"
   print('tweeting women from the MET...')

   tweepy_client.create_tweet(text=tweet_text)

tweet_women_fact(client)
