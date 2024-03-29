import datetime
import os
import csv
import tweepy
from BlockUserOptions import BlockUserOptions
from DefaultValues import DefaultValues
from Settings import Settings
import os.path
import time

class BlockManager:

    @property
    def options(self):
        return self.__block_user_options

    @options.setter
    def options(self, value):
        self.__block_user_options = value

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
                if len(row) == 0:
                    continue
                if screen_name in row[DefaultValues.SCREEN_NAME]:
                    return True

        return False

    def get_friendship(self, follower):        
        result = '' 

        if (self.__settings.restricted_accounts is None or len(self.__settings.restricted_accounts) == 0):            
            return

        print(f'Checking friendship of {follower.screen_name} ...')        
        for account in self.__settings.restricted_accounts:        
            friendship = self.__api.get_friendship(source_screen_name=follower.screen_name,target_screen_name=account)
            # Ajust it to avoid TooManyRequests.            
            self.__timer(1, show_message=False)                          
            if (friendship[0].following):
                print(f'{account} ' + u'\u2713')
                result += f'|{account}' if not result == '' else account            
            else:
                print(f'{account} ' + u'\u2715')                
            


        return result

    def __timer(self, seconds, show_message=True):
        while seconds > 0:
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
            except Exception as e:
                self.__wait(str(e)) 

    def __write_file(self, file_name, message):
        print(f'{file_name}: {message} \n\n')
        if not self.__block_user_options.dryrun:
            with open(file_name, 'a', encoding='utf-8') as f:            
                f.write(message + '\n')

    def __has_words(self, follower, word_list):

        if (word_list is None):
            return False

        return any(word.lower() in follower.description.lower().replace(',','') for word in word_list) or any(word.lower() in follower.name.lower().replace(',','') for word in word_list) 

    def __block(self, follower) -> bool:

        if (follower.favourites_count == self.__block_user_options.min_favourites_count):
            return True

        if (follower.protected == True):
            return False            

        if (self.__block_user_options.min_qty_digits_on_screen_name != 0 and len([int(s) for s in follower.screen_name if s.isdigit()]) >= self.__block_user_options.min_qty_digits_on_screen_name):
            return True

        words_found = self.__intersection(self.__settings.not_desired_words, follower.description.split())

        if (self.__block_user_options.min_restricted_words_qty <= len(words_found) and len(words_found) > 0):
            return True

        words_found = self.__intersection(self.__settings.not_desired_words, follower.name.split())            

        if (self.__block_user_options.min_restricted_words_qty <= len(words_found) and len(words_found) > 0):
            return True                                

        return False

    def __intersection(self, list1, list2):

        if (list1 is None or list2 is None):
            return []

        result = [value for value in list1 if value in list2]                         
        return result

    def __block_when_friends(self, friends) -> bool:

        if (friends is None):
            return False
        
        accounts = self.__intersection(self.__settings.restricted_accounts, friends.split('|'))  

        if (self.__block_user_options.min_restricted_accounts_qty <= len(accounts)):
            return True     

        return False
        

    def execute_block(self, follower):
        try:
            
            if self.__already_in_file(screen_name=follower.screen_name, file_name=DefaultValues.NOT_BLOCKED_FILE_NAME) or self.__already_in_file(screen_name=follower.screen_name, file_name=DefaultValues.BLOCKED_FILE_NAME):
                print(f'Already in file: {follower.screen_name}')
                return

            friends = self.get_friendship(follower) if self.__block_user_options.check_firendship else ''

            if (not follower.description is None):
                block = self.__block(follower=follower) or self.__block_when_friends(friends=friends)
                not_block = self.__has_words(follower, self.__settings.exception_words)
            else:
                block = friends != ''

            friends = f',{friends}' if friends != '' and friends != None else ''

            name = follower.name.replace(',', '-')

            follower_str = f'{follower.id_str},{name},@{follower.screen_name},{follower.created_at.strftime("%d-%m-%Y")},{follower.followers_count}{friends}'

            today = datetime.datetime.now()
            if ((today - follower.created_at.replace(tzinfo=None)).days <= 90):
                block = True
                not_block = False            

            if (follower.followers_count == 0 or (block and not not_block)):
                if not self.__block_user_options.dryrun:
                    self.__api.create_block(user_id=follower.id_str)
                self.__write_file(file_name=DefaultValues.BLOCKED_FILE_NAME, message=f'{follower_str}')
            else:
                self.__write_file(file_name=DefaultValues.NOT_BLOCKED_FILE_NAME, message=f'{follower_str}')

        except tweepy.TooManyRequests as e:
            self.__wait(str(e))                 
        except Exception as e:
            self.__wait(str(e))                                                  