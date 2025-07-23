import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import time
import threading

load_dotenv() # Load variables from .env

bot_token = os.getenv("BOT_TOKEN")
guild_id = int(os.getenv("GUILD_ID"))
channel_id = int(os.getenv("CHANNEL_ID"))

# Define intents (specify what events your bot needs to listen to)
intents = discord.Intents.default()
intents.message_content = True  # Enable if your bot needs to read message content
intents.members = True # Enable the members intent

# Create a bot instance with a command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

async def log_voice_members():
    # Get voice channel object
    await bot.fetch_channel(channel_id)
    voice_channel = bot.get_channel(channel_id)
    print(voice_channel)
    # Log once per minute
    while True:
        if voice_channel:
            for member in voice_channel.members:
                print(f"Members: {member.name}")
        time.sleep(60)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    print('------')

    # await bot.tree.sync()
    await bot.tree.sync(guild=discord.Object(guild_id))

    t1 = threading.Thread(await log_voice_members(), None)
    t1.start()

# Event handler for when a message is sent
@bot.event
async def on_message(message):
    # Runs commands before acting on message if there are any
    await bot.process_commands(message)
    # Ignores messages from the bot to prevent an infinite loop
    if message.author != bot.user:
        # Get the message content
        message_content = message.content
        print(f"Receied message: {message_content}")
        # Do something with the message content
        if "hell yeah" in message_content.lower():
            await message.channel.send("Hell Yeah!")

# A simple command
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.display_name}!")
    await ctx.send(f"You sent: {ctx.message.content}!")

@bot.command()
async def testing(ctx):
    await ctx.send("Testing")


# NEEDS A LIBRARY FOR THIS TO WORK
#------------------------------------------------
# @bot.command()
# async def connect(ctx):
#     channel = bot.get_channel(channel_id)
#     if channel:
#         await channel.connect()
#     else:
#         print(f"Channel with ID {channel_id} not found or inaccessible.")

# @bot.command()
# async def leave(ctx):
#     channel = bot.get_channel(channel_id)
#     if channel:
#         await channel.leave()
#     else:
#         print(f"Channel with ID {channel_id} not found or inaccessible.")
#------------------------------------------------
# Run the bot with your token
bot.run(bot_token)