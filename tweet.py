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

print(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

print('we loaded the auth variables')

def tweet_women_fact(tweepy_client):
    print('fetching women from the MET...')
    r1 = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/search?q=woman")
    
    parsed = r1.json()
    
    number = randint(1, 6000)

    obj_id = parsed['objectIDs'][number]

    r2 = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}")

    parsed = r2.json()

    if parsed['title'] != '':
       title = f"Title: {parsed['title']}"
    else:
        title = f"Title: Unknown"

    if parsed['artistDisplayName'] != '':
       artist = f"Artist: {parsed['artistDisplayName']}"
    else:
       artist = 'Artist: Unknown'

    if parsed['artistGender'] != '':
        gender = parsed['artistGender']
    else:
        gender = 'Artist Gender: Unknown'

    url = parsed['objectURL']

    image_url = parsed['primaryImage']
 
    img = requests.get(image_url)
    img_content = img.content
    with open('image.jpg', 'wb') as handler:
        handler.write(img_content)
   
    media = api.media_upload(filename='image.jpg')
    media_id = media.media_id

    tweet_text = f"{title}, {artist}, {gender}. See more: {url}"
    print('tweeting women from the MET...')

    tweepy_client.create_tweet(text=tweet_text, media_ids=[media_id])
    

tweet_women_fact(client)
