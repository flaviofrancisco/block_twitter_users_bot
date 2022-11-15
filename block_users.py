import os
import os.path
import tweepy
import time
from dotenv import load_dotenv, find_dotenv
import csv

BLOCKED_FILE_NAME = 'blocked.csv'
NOT_BLOCKED_FILE_NAME = 'not_blocked.csv'
SCREEN_NAME = 2

__api = None

__restricted_accounts = []
__not_desired_words = []
__exception_words = []

def already_in_file(screen_name, file_name):

    if not os.path.isfile(file_name):
        return False

    with open(file_name, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if screen_name in row[SCREEN_NAME]:
                return True

    return False

def get_api():
    auth = tweepy.OAuthHandler(consumer_key=os.getenv('consumer_key'), consumer_secret=os.getenv('consumer_secret'))
    auth.set_access_token(key=os.getenv('access_token_key'), secret=os.getenv('access_token_secret'))
    api = tweepy.API(auth, wait_on_rate_limit=False)
    return api


def block_followers():    
    for follower in limit_handled(tweepy.Cursor(__api.get_followers, screen_name=os.getenv('screen_name')).items()):        
        execute_block(follower)                    

def get_friendship(follower):
    
    result = ''   

    print(f'Checking friendship of {follower.screen_name} ...')
    for account in __restricted_accounts:        
        friendship = __api.get_friendship(source_screen_name=follower.screen_name,target_screen_name=account)
        # Ajust it to avoid TooManyRequests.
        timer(1, show_message=False)
        if (friendship[0].following):
            result += f'-{account}' if not result == '' else account            

    return result            

def execute_block(follower):
    try:

        if already_in_file(screen_name=follower.screen_name, file_name=NOT_BLOCKED_FILE_NAME) or already_in_file(screen_name=follower.screen_name, file_name=BLOCKED_FILE_NAME):
            print(f'Already in file: {follower.screen_name}')
            return

        follows = get_friendship(follower)

        if (not follower.description is None):
            block = any(word.lower() in follower.description.lower().replace(',','') for word in __not_desired_words) or follows != ''
            not_block = any(word.lower() in follower.description.lower().replace(',','') for word in __exception_words)

        follows = f',{follows}' if follows != '' else ''

        follower_str = f'{follower.id_str},{follower.name},@{follower.screen_name},{follower.created_at.strftime("%d-%m-%Y")},{follower.followers_count}{follows}'

        if (block and not not_block):
            __api.create_block(user_id=follower.id_str)
            write_file(file_name=BLOCKED_FILE_NAME, message=f'{follower_str}')
        else:
            write_file(file_name=NOT_BLOCKED_FILE_NAME, message=f'{follower_str}')

    except tweepy.TooManyRequests as e:
        wait(str(e))                 
    except tweepy.RateLimitError as e:
        wait(str(e))

def write_file(file_name, message):
    with open(file_name, 'a', encoding='utf-8') as f:
        print(f'{file_name}: {message}')
        f.write(message + '\n')

def limit_handled(cursor):
    while True:
        try:            
            yield cursor.next()
        except tweepy.TooManyRequests as e:            
            wait(str(e))
        except tweepy.RateLimitError as e:
            wait(str(e))
        except Exception as e:
            wait(str(e))            

def wait(message):
    print(message)
    timer(60 * 15)
                
def timer(seconds, show_message=True):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        if show_message:
            print(timer, end="\r")
        time.sleep(1)
        seconds -= 1


if __name__ == '__main__':    
    load_dotenv(find_dotenv())
    __restricted_accounts = os.getenv('restricted_accounts').split(',') if not os.getenv('restricted_accounts') is None else []
    __not_desired_words = os.getenv('not_desired_words').split(',') if not os.getenv('not_desired_words') is None else []
    __exception_words = os.getenv('exception_words').split(',') if not os.getenv('exception_words') is None else []
    __api = get_api()
    block_followers()
