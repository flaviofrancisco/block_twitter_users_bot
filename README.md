# Welcome to the Block Twitter Users Bot
The goal of this script is to block Twitter users based on words found in the account's description.

**It is your own responsability to run this script against your account. This code was not accurately tested.**

# Test before deploy ...
A recomendation is to play with the words in the settings: not_desired_words and exception_words **commenting the line 31 of the file: block_users.py**.
With that you generate two files: one with the blocked accounts and another one with no blocked accounts.
If you think that it is Okay, you can uncomment the line 31 of the file block_users.py.

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
restricted_accounts=[Comma separated account names of people you don't want your followers following.]
```
# Run the Script

```
$ python .\block_users.py
```

## How to set up
Play with the combination of the following env variables: **exception_words**, **not_desired_words** and **restricted_accounts**.

# Uninstall Packages
```
pip uninstall -r requirements.txt
```
or
```
pip3 uninstall -r requirements.txt
```
