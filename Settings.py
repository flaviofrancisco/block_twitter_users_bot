import os
from dotenv import load_dotenv, find_dotenv

class Settings:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.consumer_key = os.getenv('consumer_key')
        self.consumer_secret = os.getenv('consumer_secret')
        self.access_token_key = os.getenv('access_token_key')
        self.access_token_secret=os.getenv('access_token_secret')
        self.my_screen_name=os.getenv('screen_name')
        self.restricted_accounts = os.getenv('restricted_accounts').split(',') if not os.getenv('restricted_accounts') is None else []
        self.not_desired_words = os.getenv('not_desired_words').split(',') if not os.getenv('not_desired_words') is None else []
        self.exception_words = os.getenv('exception_words').split(',') if not os.getenv('exception_words') is None else []        
