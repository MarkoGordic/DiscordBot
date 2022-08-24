import os
import discord
from discord.ext import commands
import music
import musicquiz

os.environ['SPOTIPY_CLIENT_ID'] = "SPOTIFY_CLIENT_ID"
os.environ['SPOTIPY_CLIENT_SECRET'] = "SPOTIFY_CLIENT_SECRET"

cogs = [music]

client = commands.Bot(command_prefix='?', intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

cogs = [musicquiz]

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run("BOT_TOKEN")
