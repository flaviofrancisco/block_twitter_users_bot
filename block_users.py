from BlockManager import BlockManager
from BlockUserOptions import BlockUserOptions

def run():
    block_manager = BlockManager()
    
    options = BlockUserOptions()
    options.dryrun = False
    options.check_firendship = True

    block_manager.block_followers(options=options)

if __name__ == '__main__':
    run()