import discord
from discord.ext import commands
import youtube_dl


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You need to be in voice channel before using this command!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()

    @commands.command()
    async def play(self, ctx, url):
        if ctx.author.voice is None:
            await ctx.send("You need to be in voice channel before using this command!")
            return

        try:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        except discord.ext.commands.errors.ClientException:
            pass

        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio'}
        vc = ctx.voice_client

        try:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                await ctx.send("Playing " + info['title'] + " 🎶")
                track_url = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(track_url, **FFMPEG_OPTIONS)
                vc.play(source)
        except youtube_dl.utils.DownloadError:
            await ctx.send("An error occurred while playing the track. Playback stopped!")

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


def setup(client):
    client.add_cog(Music(client))
