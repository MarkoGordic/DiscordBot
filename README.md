# DiscordBot

Custom Discord bot with music quiz and music playback functionality.

## Programming Languages & Integrations
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify-1ED760?&style=for-the-badge&logo=spotify&logoColor=white)
![Youtube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)

## Requirements

- Application on [Spotify Developer Console](https://developer.spotify.com/dashboard/login) in order to get valid SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
- Bot application on [Discord Developer Portal](https://discord.com/developers/applications) in order to get valid BOT_TOKEN
- [FFmpeg](https://ffmpeg.org/)

## Installation

1. Set bot's token
2. Set parameters for proper integration with Spotify
3. Run main.py and host bot by yourself or host bot online

## Usage

Bot's command prefix is **?**

### Moderation Commands :hammer_and_wrench:

- `?kick member_mention` -> bot will kick mentioned member if you have needed permissions
- `?ban member_mention` -> bot will ban mention member if you have needed permissions

### Voice Chat Commands :microphone:

- `?join` -> bot will join voice channel you're in
- `?leave` -> bot will disconnect from voice channel

### Music Quiz Commands :notes:

- `?startquiz spotify_URI rounds` -> starts music quiz with specified number of rounds using tracks from given Spotify playlist
- `?skip` -> vote for skip for currently playing track

### Music Playback Commands :musical_note:

- `?play url` -> play song from valid Youtube URL

## Licence

Released under the [MIT](https://choosealicense.com/licenses/mit/) license.
