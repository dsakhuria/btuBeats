import discord
from discord.ext import commands
import yt_dlp


intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice
    if voice_channel is None or voice_channel.channel is None:
        await ctx.send("**[!!]**You need to be in a voice channel to use this command.")
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_connected():
        await voice_client.move_to(voice_channel.channel)
    else:
        voice_client = await voice_channel.channel.connect()

    ydl_opts = {'format': 'bestaudio/best',
                'noplaylist': True, #no playlist    
                'extract_audio': False #ffmpeg roar sheinaxos
                }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(url2))

@bot.command()
async def skip(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()

@bot.command()
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
    await voice_client.disconnect()

@bot.command()
async def disconnect(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await voice_client.disconnect()

@bot.command()
async def bot_help(ctx):
    # Customize the help message based on your bot's commands
    help_message = "**Available commands**:\n" \
                   "**!play [url]** - Play music from a YouTube URL\n" \
                   "**!skip** - Skip the current song\n" \
                   "**!stop** - Stop playing music and disconnect\n" \
                   "**!disconnect** - Disconnect from the voice channel\n" \
                   "**!bot_help** - Show this help message"
    await ctx.send(help_message)








bot.run('#Bot token removed, as it can be stolen(replace it with urs)')
