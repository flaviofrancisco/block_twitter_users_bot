class BlockUserOptions:
    def __init__(self):
        
        self.dryrun = True
        '''If true runs on test mode.'''

        self.check_firendship = False
        '''If true checks whether  the follower is following accounts listed on the env. variable: restricted_accounts and blocks if applicable. '''

        self.min_restricted_words_qty = 1
        '''Minimum quantity of words from the env. variable: not_desired_words either found either in the name or account description to block a user. '''

        self.min_restricted_accounts_qty = 1
        '''Minimum quantity of restricted accounts from the env. variable: restricted_accounts that a follower follows to block a user. '''

        self.min_tweets_from_user = 0
        '''If your follower has no Tweets than she or he will be blocked.'''

        self.min_favourites_count = 0
        '''If the follower has no reaction than will be blocked.'''

