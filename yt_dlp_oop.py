import discord
from discord.ext import commands
import yt_dlp


class MusicBot(commands.Bot):

    def __init__(self, command_prefix='!', intents=discord.Intents.default()):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.ytdl = yt_dlp.YoutubeDL()

    @commands.command()
    async def play(self, ctx, url):
        voice_channel = ctx.author.voice
        if voice_channel is None or voice_channel.channel is None:
            await ctx.send("**[!!]**You need to be in a voice channel to use this command.")
            return

        voice_client = self.get_voice_client(ctx.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(voice_channel.channel)
        else:
            voice_client = await voice_channel.channel.connect()

        info = self.ytdl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(url2))

    @commands.command()
    async def skip(self, ctx):
        voice_client = self.get_voice_client(ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()

    @commands.command()
    async def stop(self, ctx):
        voice_client = self.get_voice_client(ctx.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()
        await voice_client.disconnect()

    @commands.command()
    async def disconnect(self, ctx):
        await self.get_voice_client(ctx.guild).disconnect()

    @commands.command()
    async def bot_help(self, ctx):
        # Customize the help message based on your bot's commands
        help_message = "**Available commands**:\n" \
                   "**!play [url]** - Play music from a YouTube URL\n" \
                   "**!skip** - Skip the current song\n" \
                   "**!stop** - Stop playing music and disconnect\n" \
                   "**!disconnect** - Disconnect from the voice channel\n" \
                   "**!bot_help** - Show this help message"
        await ctx.send(help_message)


if __name__ == '__main__':
    bot = MusicBot()
    bot.run('#Bot token removed, as it can be stolen(replace it with urs)')
