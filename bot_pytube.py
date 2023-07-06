import discord
from discord.ext import commands
import os
import pytube

# Create a Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Global variables
is_playing = False
voice_channel = None

@client.event
async def on_ready():
    print('Boti Gaeshva.')

@client.event()
async def help(ctx):
    embed = discord.Embed(title="Help - Available Commands", description="Here are the available commands:", color=discord.Color.blue())
    embed.add_field(name="!play [song]", value="Plays a song from YouTube", inline=False)
    embed.add_field(name="!pause", value="Pauses the currently playing song", inline=False)
    embed.add_field(name="!resume", value="Resumes the paused song", inline=False)
    embed.add_field(name="!stop", value="Stops playing the current song", inline=False)
    embed.add_field(name="!skip", value="Skips the current song and plays the next one", inline=False)
    embed.add_field(name="!help", value="Displays this help message", inline=False)

    await ctx.send(embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!play'):
        query = message.content[6:]
        await play_music(query, message)

    elif message.content == '!pause':
        if is_playing:
            voice_channel.pause()
            await message.channel.send('Playback paused.')
        else:
            await message.channel.send('Nothing is playing.')

    elif message.content == '!resume':
        if is_playing:
            voice_channel.resume()
            await message.channel.send('Playback resumed.')
        else:
            await message.channel.send('Nothing is playing.')

    elif message.content == '!stop':
        if is_playing:
            voice_channel.stop()
            await message.channel.send('Playback stopped.')
        else:
            await message.channel.send('Nothing is playing.')

async def play_music(query, message):
    global is_playing
    global voice_channel

    voice_channel = message.author.voice.channel

    try:
        await voice_channel.connect()
    except discord.errors.ClientException:
        pass

    try:
        search_results = pytube.Search(query)
        video_url = search_results[0].url

        yt = pytube.YouTube(video_url)
        audio_stream = yt.streams.get_audio_only()

        voice_channel.play(discord.FFmpegPCMAudio(audio_stream.url))
        is_playing = True

        await message.channel.send(f'Now playing: {yt.title}')

    except pytube.exceptions.RegexMatchError:
        await message.channel.send('An error occurred while trying to search for the video.')
    except IndexError:
        await message.channel.send('No search results found.')

@client.event
async def on_voice_state_update(member, before, after):
    global is_playing
    global voice_channel

    if member == client.user and after.channel is None:
        is_playing = False
        voice_channel = None
        await client.voice_clients[0].disconnect()


client.run('#Bot token removed, as it can be stolen(replace it with urs)')
