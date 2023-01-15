from BlockManager import BlockManager
from BlockUserOptions import BlockUserOptions

def run():
    block_manager = BlockManager()
    
    options = BlockUserOptions()
    options.dryrun = True
    options.check_firendship = True
    options.min_restricted_accounts_qty = 2
    options.min_restricted_words_qty = 2 
    options.min_qty_digits_on_screen_name = 5
    options.min_favourites_count = 0
      
    block_manager.block_followers(options=options)

if __name__ == '__main__':    
        run()