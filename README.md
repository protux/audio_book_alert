# Executing the program
If you just want to run the software this is the right chapter for you. For setting up a development environment see the chapters below.

## Customize it for your needs
At first you need to choose which Authors and Narrators you want to be notified about. There is a file called `author_names` and a file called `narrator_names`. It's pretty easy: authors you want to be notified about need to be appended to `author_names` and narrators you want to be notified about need to be appended to `narrator_names`.


## Set up your telegram bot
To run the software you need a telegram bot and add the bots config to your environment.

To create a telegram bot you need to talk to [the Botfather](https://core.telegram.org/bots#3-how-do-i-create-a-bot), but make sure you pay him respect. Ask him for a name and an API-Key. It's obvious, that he won't do it for nothing.

After the Botfather granted you an own bot you need to put it's credentials to the environment. To do this you need to fill the following environment variables:
- `ABA_TELEGRAM_BOT_NAME=${NAME_OF_YOUR_BOT}`
- `ABA_TELEGRAM_API_KEY=${YOUR_BOT_API_KEY}`

## Start the bot
To start the bot you just need to run 
```
PYTHONPATH=${PYTHONPATH}:${REPOSITORY_ROOT} python audio_book_alert --bot-mode
```
This script needs to run permanently, so you can subscribe. Technically, you can stop this script after you subscribed if there will be no other people using it.

## Check for new audio books and alert subscribers
Now all preconditions are met. To check for new audio books just set up a cronjob which regularly runs  
```
PYTHONPATH=${PYTHONPATH}:${REPOSITORY_ROOT} python audio_book_alert
```
This script will check for new audio books and will notify subscribers about it.

# Development
The following chapters should give you all the information to contribute or adapt the software to your needs.

## Setting up a virtual environment
For this project `pip` is used. To set it up please follow the next steps: 
- Create new venv: run `python -m venv venv` in the root of this repository  
- Activate it with `source venv/bin/activate`
- Update pip etc. `pip install -U pip wheel setuptools`
- Install dependencies: `pip install -r requirements.txt`

## Set up PyCharm
PyCharm is what I am currently using - so the IDE is a bit biased. To use it please follow the next steps:
- Add the venv created above as project environment by setting its python binary as `Project Interpreter` in project settings.
- Add a runtime environment for a python script named "Telegram Bot"
  - Script Path: `${REPOSITORY}/audio_book_alert`
  - Parameters: `--bot-mode`
  - Environment Variables: 
    - `ABA_TELEGRAM_BOT_NAME=${NAME_OF_YOUR_BOT}`
    - `ABA_TELEGRAM_API_KEY=${YOUR_BOT_API_KEY}`
- Add a runtime environment for a python script "Audiobook Alert"
  - Script Path: `${REPOSITORY}/audio_book_alert`
  - Environment Variables: 
    - `ABA_TELEGRAM_BOT_NAME=${NAME_OF_YOUR_BOT}`
    - `ABA_TELEGRAM_API_KEY=${YOUR_BOT_API_KEY}`

# TODO in Readme
- explain how to start telegram bot
- explain how to activate scraper
- explpain how to add narrators/ authors

# TODO in code
- write file for starting telegram bot as systemd service
- move storage to database and not text file full of json
- make authors and narrators configurable more dynamically