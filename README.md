# Welcome to the Block Twitter Users Bot
The goal of this script is to block Twitter users based on words found in the account's description and based on account that your followers follow.
Due to rate limits the program stops for 15 minutes each time that either an Rate limit exception or Too Many Request exception is thrown.

**IT IS YOUR RESPONSABILITY TO RUN THIS SCRIPT AGAINST YOUR ACCOUNT. THIS CODE WAS NOT ACCURATELY TESTED**

**I cannot guarantee that it will work as you expect.**

# How to create a bot with Python using Tweepy

[Como criar um bot no Twitter](https://www.youtube.com/watch?v=RijhM5PFyOA)

[How to Create a Twitter Bot [Tweepy with Python]](https://www.youtube.com/watch?v=w_e1ZhwCBgc)

[Create The Ultimate Twitter Bot With Python In 30 Minutes](https://www.youtube.com/watch?v=ewq-91-e2fw)

# Test before deploy ...

In order to test please update the code in the file: block_users.py

```python
block_manager.block_followers(check_firendship=False, dryrun=True)
```

If you either don't wan't to check your followers friendship set the check_firendship parameter to False. If that parameter is True it will increase your Twitter rate consumption and it will slow down the applicaiton.

# Setting up your environment
After cloning this repository you should create a virtual environment and activate it.

## Create a virtual environment

Create a virtual environment and activate it.

```
$ python -m venv venv
$ .\venv\Scripts\activate
```

# Install Packages

Install the dependencies with the environment activated to avoid install it globally in your machine.
```
$ pip install -r requirements.txt
```
or

```
$ pip3 install -r requirements.txt
```

# Run the Script Replace the values between squared brackets accordingly.

Rename the file: .env.template to .env and fill up the values of the enviroment variables based on your needs.

```
consumer_key=[Get it from the Twitter Developer Console]
consumer_secret=[Get it from the Twitter Developer Console]
access_token_key=[Get it from the Twitter Developer Console]
access_token_secret=[Get it from the Twitter Developer Console]
screen_name=[Your account]
not_desired_words=[Comma separated word list]
exception_words=[Comma separated word list]
restricted_accounts=[Comma separated account names of people you don't want your followers following.]
```
# Run the Script

```
$ python .\block_users.py
```

## How to set up
Play with the combination of the following env variables: **exception_words**, **not_desired_words** and **restricted_accounts**.

If you want to block followers with the following words: war,crime,virus in their description:
```
not_desired_words=war,crime,virus
```

But don't want to block if they have the words: united nations
```
exception_words=united nations
```

Also, block if they follow these accounts: @xxx, @abc1234, @ert23455 (don't use the symbol at).
```
restricted_accounts=xxx,abc1234,ert23455
```

# Uninstall Packages
```
pip uninstall -r requirements.txt
```
or
```
pip3 uninstall -r requirements.txt
```

# Notes

The use of the function: **get_friendship** my impact in your Tweeter API rate limit. If you want you can either remove it or change the function in a way that exist if at least one result is true in order to compare will all values.
