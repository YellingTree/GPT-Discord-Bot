from discord.ext import commands
from discord.utils import get
import manager
import config

bot = commands.Bot(command_prefix=config.chat_prefix, intents=config.bot_intents)


@bot.command(name='gpt')
async def gpt(ctx, *, user_message: str = ""):
    if ctx.guild is None:
        server_id = ctx.author.id
    else:
        server_id = ctx.guild.id
    conversation = await manager.MemoryManagment.get_conversation(server_id)
    user_message = {"role": "user", "content": user_message}
    response, failstate = await manager.ResponseManagemnt.create_response(server_id, conversation, user_message)
    message_blocks = await manager.ResponseManagemnt.create_messages(server_id, response, conversation, user_message, failstate)
    for block in message_blocks:
        await ctx.send(block)
@bot.command(name='reset')
async def reset(ctx):
    if ctx.guild is None:
        server_id = ctx.author.id
    else:
        server_id = ctx.guild.id
    await manager.MemoryManagment.save_conversation(server_id, [])
    await ctx.send("Conversation reset, memory cleared.")

@bot.event
async def on_message(message):
    if message.author != bot.user:
        ctx = await bot.get_context(message)
        if bot.user.mentioned_in(message):
            mention_string = f'<@{bot.user.id}>'
            user_message = message.content
            user_message = user_message.replace(mention_string, config.mention_replacement)
            await gpt(ctx, user_message=message.content)
        if message.reference and message.reference.resolved.author == bot.user:
            await gpt(ctx, user_message=message.content)
    if message.author != bot.user and message.guild is None:
        ctx = await bot.get_context(message)
        if ctx.message.content.startswith("!reset"):
            await reset(ctx)
        else:
            await gpt(ctx, user_message=message.content)
    else:
        await bot.process_commands(message)
    
bot.run(config.discord_bot_token)