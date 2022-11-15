import os
import csv
import tweepy
from DefaultValues import DefaultValues
from Settings import Settings
import os.path
import time

class BlockManager:

    def __init__(self):
        
        self.__settings = Settings()
        
        auth = tweepy.OAuthHandler(consumer_key=self.__settings.consumer_key, consumer_secret=self.__settings.consumer_secret)
        auth.set_access_token(key=self.__settings.access_token_key, secret=self.__settings.access_token_secret)
        self.__api = tweepy.API(auth, wait_on_rate_limit=False)        

    def __already_in_file(self, screen_name, file_name):

        if not os.path.isfile(file_name):
            return False

        with open(file_name, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if screen_name in row[DefaultValues.SCREEN_NAME]:
                    return True

        return False

    def get_friendship(self, follower):
        
        result = ''   
        dot = '.'
        print(f'Checking friendship of {follower.screen_name} ...')        
        for account in self.__settings.restricted_accounts:        
            friendship = self.__api.get_friendship(source_screen_name=follower.screen_name,target_screen_name=account)
            # Ajust it to avoid TooManyRequests.            
            self.__timer(1, show_message=False)              
            print(dot, end="\r")                      
            print(dot)
            if (friendship[0].following):
                result += f'-{account}' if not result == '' else account            
            dot += '.'            


        return result

    def __timer(self, seconds, show_message=True):
        while seconds:
            mins, secs = divmod(seconds, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            if show_message:
                print(timer, end="\r")
            time.sleep(1)
            seconds -= 1  

    def __wait(self, message):
        print(message)
        self.__timer(60 * 15)                          

    def block_followers(self):    
        for follower in self.__limit_handled(tweepy.Cursor(self.__api.get_followers, screen_name=self.__settings.my_screen_name).items()):        
            self.execute_block(follower) 

    def __limit_handled(self, cursor):
        while True:
            try:            
                yield cursor.next()
            except tweepy.TooManyRequests as e:            
                self.__wait(str(e))
            except tweepy.RateLimitError as e:
                self.__wait(str(e))
            except Exception as e:
                self.__wait(str(e)) 

    def __write_file(self, file_name, message):
        with open(file_name, 'a', encoding='utf-8') as f:
            print(f'{file_name}: {message}')
            f.write(message + '\n') 

    def execute_block(self, follower):
        try:

            if self.__already_in_file(screen_name=follower.screen_name, file_name=DefaultValues.NOT_BLOCKED_FILE_NAME) or self.__already_in_file(screen_name=follower.screen_name, file_name=DefaultValues.BLOCKED_FILE_NAME):
                print(f'Already in file: {follower.screen_name}')
                return

            follows = self.get_friendship(follower)

            if (not follower.description is None):
                block = any(word.lower() in follower.description.lower().replace(',','') for word in self.__settings.not_desired_words) or follows != ''
                not_block = any(word.lower() in follower.description.lower().replace(',','') for word in self.__settings.exception_words)

            follows = f',{follows}' if follows != '' else ''

            name = follower.name.replace(',', '-')

            follower_str = f'{follower.id_str},{name},@{follower.screen_name},{follower.created_at.strftime("%d-%m-%Y")},{follower.followers_count}{follows}'

            if (block and not not_block):
                self.__api.create_block(user_id=follower.id_str)
                self.__write_file(file_name=DefaultValues.BLOCKED_FILE_NAME, message=f'{follower_str}')
            else:
                self.__write_file(file_name=DefaultValues.NOT_BLOCKED_FILE_NAME, message=f'{follower_str}')

        except tweepy.TooManyRequests as e:
            self.__wait(str(e))                 
        except tweepy.RateLimitError as e:
            self.__wait(str(e))                                                  