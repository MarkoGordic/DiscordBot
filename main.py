import os
import discord
from discord.ext import commands
from cogs import moderation, music, musicquiz

os.environ['SPOTIPY_CLIENT_ID'] = "SPOTIFY_CLIENT_ID"
os.environ['SPOTIPY_CLIENT_SECRET'] = "SPOTIFY_CLIENT_SECRET"

client = commands.Bot(command_prefix='?', intents=discord.Intents.all())

cogs = [music, musicquiz, moderation]

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run("BOT_TOKEN")
