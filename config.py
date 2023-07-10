import discord
import discord.ext

bot_intents = discord.Intents.default()
bot_intents.message_content = True

discord_bot_token = '' #Token for your discord bot
openai_api_key = ("") #Your OpenAI API key

chat_prefix = "!" #Command prefix for the bot ex. !gpt /gpt .gpt 
mention_replacement = "ChatGPT" #Replaces the @BotName mention ID (<@126317676491>) with a name
old_msg_removal_amount = 10 #How many of the oldest messages to remove when the bot reaches it's token limit
delete_empty_messages = True #Should messages that consist of empty strings or only spaces be removed?
remove_error_messages = True #Save error messages to the conversation?
chat_model = "gpt-4" #OpenAI chat compleation model
token_limit = 1500 #Max token limit per generation
top_prob = .9 #top_p variable, refer to this doc: https://platform.openai.com/docs/api-reference/chat/create#chat/create-top_p
bias = {"21017": -100} #Determins what tokens the bot should be biased too, example is the token for ### has a 0% chance of being generated.
max_characters = 2000 #Discords Max Character limit
creation_amount = 1 #How many generations should be created per request

system_message = "Be a helpful chatbot." #System messages, sets a note for the chatbot to indicate it's function
