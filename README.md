# GPT-Discord-Bot
Discord Bot that interfaces with OpenAI's Chat Completion models such as GPT-4, GPT-3.5, etc

# Setup:
## First enter your information in the config.py file, including your OpenAI API key, Discord Bot Token, and Select which model you would like to use (GPT-4, GPT-3.5, etc).
There are a few other settings to change in the config file such as model variables and history keeping.

# How to use
Once you have entered your information into the config.py file all that is needed is to run the client.py and the bot should connect to discord servers.

# Notes:
You will need to get your own API key from OpenAI and create your own discord bot through https://discord.com/developers.

#### Creating the Discord Bot:
Presence Intent: Enabled - found under App -> Bot -> Toggle for Presence Intent


Creating URL: OAuth2 -> URL Generator -> Check box for bot under Scope. Under Bot Permissions check boxes for Read Messages/View Channels, and Send Messages  
