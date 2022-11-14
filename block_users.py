import os
import tweepy
import time
from dotenv import load_dotenv, find_dotenv

__api = None

def get_api():
    auth = tweepy.OAuthHandler(consumer_key=os.getenv('consumer_key'), consumer_secret=os.getenv('consumer_secret'))
    auth.set_access_token(key=os.getenv('access_token_key'), secret=os.getenv('access_token_secret'))
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def block_followers():

    for follower in limit_handled(tweepy.Cursor(__api.get_followers, screen_name=os.getenv('screen_name')).items()):
        execute_block(follower)
                                                

def execute_block(follower): 

    not_desired_words = os.getenv('not_desired_words').split(',')
    exception_words = os.getenv('exception_words').split(',')

    block = any(word.lower() in follower.description.lower() for word in not_desired_words)
    not_block = any(word.lower() in follower.description.lower() for word in exception_words)

    follower_str = f'@{follower.screen_name},{follower.created_at.strftime("%d-%m-%Y")},{follower.followers_count}'

    if (block and not not_block):
        __api.create_block(user_id=follower.id_str)
        with open('blocked.csv', 'a', encoding='utf-8') as f:
            print(f'BLOCKED --> {follower_str}')
            f.write(follower_str + '\n')
    else:
        with open('not_blocked.csv', 'a', encoding='utf-8') as f:
            print(f'OK {follower_str}')
            f.write(follower_str + '\n')
  
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except Exception as e:
            timer(15 * 60)
            print(str(e))

def timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1


if __name__ == '__main__':   
    load_dotenv(find_dotenv())  
    __api = get_api() 
    block_followers()
