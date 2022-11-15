import os
import tweepy
import time
from dotenv import load_dotenv, find_dotenv

__api = None


def get_api():
    auth = tweepy.OAuthHandler(consumer_key=os.getenv(
        'consumer_key'), consumer_secret=os.getenv('consumer_secret'))
    auth.set_access_token(key=os.getenv('access_token_key'),
                          secret=os.getenv('access_token_secret'))
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def block_followers():    
    for follower in limit_handled(tweepy.Cursor(__api.get_followers, screen_name=os.getenv('screen_name')).items()):
        execute_block(follower)


def get_friendship(follower):
    
    result = ''

    accounts = os.getenv('restricted_accounts').split(',') if not os.getenv('restricted_accounts') is None else None

    if (accounts is None):
        return result

    for account in accounts:
        friendship = __api.get_friendship(source_screen_name=follower.screen_name,target_screen_name=account)
        if (friendship[0].following):
            result += f'-{account}' if not result == '' else account

    return result


def execute_block(follower):

    not_desired_words = os.getenv('not_desired_words').split(',')
    exception_words = os.getenv('exception_words').split(',')

    follows = get_friendship(follower)

    if (not follower.description is None):
        block = any(word.lower() in follower.description.lower().replace(',','') for word in not_desired_words) or follows != ''
        not_block = any(word.lower() in follower.description.lower().replace(',','') for word in exception_words)

    follows = f',{follows}' if follows != '' else ''

    follower_str = f'{follower.id_str},{follower.name},@{follower.screen_name},{follower.created_at.strftime("%d-%m-%Y")},{follower.followers_count}{follows}'

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
            print(str(e))
            timer(15 * 60)            


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
