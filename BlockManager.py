import os
import csv
import tweepy
from BlockUserOptions import BlockUserOptions
from DefaultValues import DefaultValues
from Settings import Settings
import os.path
import time

class BlockManager:

    def __init__(self):
        self.__block_user_options = BlockUserOptions()        
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

    def block_followers(self, options: BlockUserOptions):
        """ Scan all your followers and blocks each follower based on the values filled in your environment variables:
        e.g:
            - not_desired_words: comma separated values.
            - exception_words: comma separated values.
            - restricted_accounts: comma separeted Twitter account names.

        Args:
        options: BlockUserOptions type where you can set you preferences, please see more in the file: BlockUserOptions.py.
        """  
        self.__block_user_options = options

        for follower in self.__limit_handled(tweepy.Cursor(self.__api.get_followers, screen_name=self.__settings.my_screen_name, count=200).items()):        
            self.execute_block(follower) 

    def __limit_handled(self, cursor):
        while True:
            try:            
                yield cursor.next()
            except tweepy.TooManyRequests as e:            
                self.__wait(str(e))
            except Exception as e:
                self.__wait(str(e)) 

    def __write_file(self, file_name, message):
        print(f'{file_name}: {message}')
        if not self.__block_user_options.dryrun:
            with open(file_name, 'a', encoding='utf-8') as f:            
                f.write(message + '\n')

    def __has_words(self, description, word_list):
        return any(word.lower() in description.lower().replace(',','') for word in word_list)             

    def execute_block(self, follower):
        try:

            if self.__already_in_file(screen_name=follower.screen_name, file_name=DefaultValues.NOT_BLOCKED_FILE_NAME) or self.__already_in_file(screen_name=follower.screen_name, file_name=DefaultValues.BLOCKED_FILE_NAME):
                print(f'Already in file: {follower.screen_name}')
                return

            follows = self.get_friendship(follower) if self.__block_user_options.check_firendship else ''

            if (not follower.description is None):
                block = self.__has_words(follower.description, self.__settings.not_desired_words) or follows != ''
                not_block = self.__has_words(follower.description, self.__settings.exception_words)
            else:
                block = follows != ''

            follows = f',{follows}' if follows != '' else ''

            name = follower.name.replace(',', '-')

            follower_str = f'{follower.id_str},{name},@{follower.screen_name},{follower.created_at.strftime("%d-%m-%Y")},{follower.followers_count}{follows}'

            if (block and not not_block):
                if not self.__block_user_options.dryrun:
                    self.__api.create_block(user_id=follower.id_str)
                self.__write_file(file_name=DefaultValues.BLOCKED_FILE_NAME, message=f'{follower_str}')
            else:
                self.__write_file(file_name=DefaultValues.NOT_BLOCKED_FILE_NAME, message=f'{follower_str}')

        except tweepy.TooManyRequests as e:
            self.__wait(str(e))                 
        except Exception as e:
            self.__wait(str(e))                                                  