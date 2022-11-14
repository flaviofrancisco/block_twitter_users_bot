# Welcome to the Block Twitter Users Bot
The goal of this script is to block Twitter users based on words found in the account's description.

# Setting up your environment
After cloning this repository you should create a virtual environment and activate it.

# Install Packages

```
$ pip install -r requirements.txt
```
or

```
$ pip3 install -r requirements.txt
```

## .env file
You should also create a .env file with the following keys/ values based on your needs. Replace the values between squared brackets accordingly.

```
consumer_key=[Get it from the Twitter Developer Console]
consumer_secret=[Get it from the Twitter Developer Console]
access_token_key=[Get it from the Twitter Developer Console]
access_token_secret=[Get it from the Twitter Developer Console]
screen_name=[Your account]
not_desired_words=[Comma separated word list]
exception_words=[Comma separated word list]
```
