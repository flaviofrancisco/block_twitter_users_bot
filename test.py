
import tweepy
from BlockManager import BlockManager
from BlockUserOptions import BlockUserOptions
from Settings import Settings


def test():

    user = api.get_user(screen_name='User Twitter account')

    options = BlockUserOptions()
    options.dryrun = False
    options.check_firendship = True
    options.min_restricted_accounts_qty = 2
    options.min_restricted_words_qty = 2

    block_manager = BlockManager()  
    block_manager.options = options  
    block_manager.execute_block(user)


if __name__ == '__main__':
        
    settings = Settings()        
    auth = tweepy.OAuthHandler(consumer_key=settings.consumer_key, consumer_secret=settings.consumer_secret)
    auth.set_access_token(key=settings.access_token_key, secret=settings.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=False) 
    test()   
    