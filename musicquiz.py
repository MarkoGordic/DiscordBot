import time
import discord
from discord.ext import commands
import youtube_dl
import spotipy
import random

timeout_time = 5
quiz_playlist = []


class MusicQuiz(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.vc = None
        self.voice_channel = None
        self.quiz_ctx = None
        self.quiz_channel = None
        self.is_running = False
        self.skippers = []
        self.leaderboard = {}
        self.track_name_guessed = False
        self.artist_name_guessed = False
        self.artist_names = []
        self.track_names = []

        @client.event
        async def on_message(message):
            if message.channel.id == self.quiz_channel:
                if message.content != "":
                    user_message = str.lower(str(message.content))

                    if str.lower(str(self.track_names[0])) in user_message and str.lower(str(self.artist_names[0])) in user_message:
                        correct = str.lower(str(self.track_names[0])) + " " + str.lower(str(self.artist_names[0]))
                        correct_rev = str.lower(str(self.artist_names[0])) + " " + str.lower(str(self.track_names[0]))
                        if user_message == correct or user_message == correct_rev:
                            if not self.track_name_guessed:
                                self.track_name_guessed = True

                                if str(message.author) in self.leaderboard:
                                    self.leaderboard[str(message.author)] = self.leaderboard[str(message.author)] + 1
                                else:
                                    self.leaderboard[str(message.author)] = 1

                                await self.quiz_ctx.send(message.author.mention + " guessed track name!")

                            if not self.artist_name_guessed:
                                self.artist_name_guessed = True

                                if str(message.author) in self.leaderboard:
                                    self.leaderboard[str(message.author)] = self.leaderboard[str(message.author)] + 1
                                else:
                                    self.leaderboard[str(message.author)] = 1

                                await self.quiz_ctx.send(message.author.mention + " guessed artist name!")
                    elif user_message == str.lower(str(self.track_names[0])) and not self.track_name_guessed:
                        self.track_name_guessed = True

                        if str(message.author) in self.leaderboard:
                            self.leaderboard[str(message.author)] = self.leaderboard[str(message.author)] + 1
                        else:
                            self.leaderboard[str(message.author)] = 1

                        await self.quiz_ctx.send(message.author.mention + " guessed track name!")
                    elif user_message == str.lower(str(self.artist_names[0])) and not self.artist_name_guessed:
                        self.artist_name_guessed = True

                        if str(message.author) in self.leaderboard:
                            self.leaderboard[str(message.author)] = self.leaderboard[str(message.author)] + 1
                        else:
                            self.leaderboard[str(message.author)] = 1

                        await self.quiz_ctx.send(message.author.mention + " guessed artist name!")
                    if self.track_name_guessed and self.artist_name_guessed:
                        await self.next_track()

            await client.process_commands(message)

    @commands.command()
    async def skip(self, ctx):
        if ctx.message.author in self.skippers:
            ctx.send("You already voted to skip!")
        else:
            members = 0
            for member in self.voice_channel.members:
                if not member.bot:
                    members += 1

            self.skippers.append(ctx.message.author)

            if len(self.skippers) >= int(members):
                await ctx.send("Skipping track!")
                await self.next_track()
            else:
                await ctx.send(ctx.message.author.mention + " voted to skip! " + str(members - len(self.skippers)) + " vote(s) to skip!")

    async def end_quiz(self):
        await self.vc.disconnect()
        sorted_leaderboard = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)

        if len(sorted_leaderboard) > 0:
            results = "Quiz has ended! These are the results:\n\n"
            curr = 1

            for i in sorted_leaderboard:
                if curr == 1:
                    results += "🥇 " + str(i[0]) + " with " + str(i[1]) + " points\n\n"
                elif curr == 2:
                    results += "🥈 " + str(i[0]) + " with " + str(i[1]) + " points\n\n"
                elif curr == 3:
                    results += "🥉 " + str(i[0]) + " with " + str(i[1]) + " points\n\n"
                else:
                    results += str(curr) + ". " + str(i[0]) + " with " + str(i[1]) + " points\n"
                curr += 1

            await self.quiz_ctx.send(results)
        else:
            await self.quiz_ctx.send("Quiz has ended! No one got any points!")

        self.artist_name_guessed = False
        self.track_name_guessed = False
        self.quiz_ctx = None
        self.quiz_channel = None
        self.voice_channel = None
        return

    # TODO: Find better solution for detecting and handling playback errors
    def check_playback_timeout(self):
        time.sleep(timeout_time)  # In case playback don't start in time, timeout will occur

        return not self.vc.is_playing()

    async def next_track(self):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio'}

        download_error = False
        self.vc.stop()
        self.skippers = []
        self.track_name_guessed = False
        self.artist_name_guessed = False

        try:
            if len(quiz_playlist) > 0:
                try:
                    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(f"ytsearch:{quiz_playlist[0]}", download=False)['entries'][0]['formats'][0]['url']
                        source = discord.FFmpegOpusAudio(info, **FFMPEG_OPTIONS)
                        self.vc.play(source, after=lambda: self.next_track())
                except youtube_dl.utils.DownloadError:
                    download_error = True

                if not self.is_running:
                    self.is_running = True
                else:
                    await self.quiz_ctx.send("The track was " + self.track_names[0] + " by " + self.artist_names[0] + " !")
                    self.track_names.pop(0)
                    self.artist_names.pop(0)

                if self.track_names[0] == '':
                    self.track_name_guessed = True

                if self.artist_names[0] == '':
                    self.artist_name_guessed = True

                quiz_playlist.pop(0)

                playback_error = self.check_playback_timeout()

                if download_error or playback_error:
                    await self.quiz_ctx.send("An error occurred while playing the track. Skipping track!")
                    await self.next_track()
            else:
                if self.is_running:
                    self.is_running = False
                    await self.end_quiz()
        except IndexError:
            pass

    @commands.command()
    async def startquiz(self, ctx, uri, rounds):
        if self.is_running:
            await ctx.send("Quiz iz already running!")
            return

        await ctx.send("Starting music quiz! Please be patient.")

        try:
            self.voice_channel = ctx.author.voice.channel
            await self.voice_channel.connect()
        except discord.ext.commands.errors.ClientException:
            pass

        self.vc = ctx.voice_client
        self.quiz_ctx = ctx
        self.leaderboard = {}
        self.artist_names = []
        self.track_names = []

        auth_manager = spotipy.SpotifyClientCredentials()
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        self.quiz_channel = ctx.message.channel.id

        # [0] - "spotify", [1] - content type, [2] - id
        params = uri.split(':')

        if params[1] == "track":
            ctx.send("You need to provide a playlist URI, not a track URI!")
        else:
            # fetching playlist tracks
            result = spotify.playlist(params[2], fields=None, market=None, additional_types=('track',))
            tracks = result['tracks']['items']

            if int(rounds) > len(tracks):
                await ctx.send("INFO : The number of rounds is higher than the number of tracks in the playlist. Some tracks will repeat.")

            tmp_indexes = []

            for i in range(int(rounds)):
                if int(rounds) <= len(tracks):
                    while True:
                        index = random.randint(0, len(tracks) - 1)
                        if index not in tmp_indexes:
                            tmp_indexes.append(index)
                            break
                else:
                    index = random.randint(0, len(tracks) - 1)

                artist = tracks[index]['track']['artists'][0]['name']
                track_name = tracks[index]['track']['name']

                self.artist_names.append(artist)
                self.track_names.append(track_name)

                quiz_playlist.append(artist + " " + track_name + " Lyrics")  # appending lyrics to avoid music videos

            await self.next_track()


def setup(client):
    client.add_cog(MusicQuiz(client))
