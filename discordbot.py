from discord.ext import commands
import os
import traceback
import discord
import asyncio
import urllib.parse
import re
import youtube_dl

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='@', intents=intents)
token = os.environ['DISCORD_BOT_TOKEN']
embed = discord.Embed()
embed.color = discord.Color.blue()
lang = os.getenv('DISCORD_BOT_LANG', default='ja')
channel_id = {}


setlist_dic = {}
loop_flag_dic = {}
now_music = {}

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.time = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()


    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))
    @commands.command(aliases=["fs", "s"])
    async def skip(self, ctx):
        global now_music
        guild_id = ctx.guild.id
        if loop_flag_dic[guild_id]:
            now_music[guild_id] = setlist_dic[guild_id].pop(0)
        await ctx.send(":fast_forward: Skipped :thumbsup:")
        await ctx.voice_client.pause()

    @commands.command()
    async def start(self, ctx):
        await ctx.voice_client.resume()

    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        guild_id = ctx.guild.id
        await ctx.send(setlist_dic[guild_id])

    @commands.command(aliases=["np"])
    async def nowplaying(self, ctx):
        guild_id = ctx.guild.id
        await ctx.send(now_music[guild_id])

    @commands.command()
    async def loop(self, ctx):
        global loop_flag_dic
        guild_id = ctx.guild.id
        if loop_flag_dic[guild_id]:
            loop_flag_dic[guild_id] = False
            await ctx.send("🔂 **Disabled!**")
        else:
            loop_flag_dic[guild_id] = True
            await ctx.send("🔂 **Enabled!**")
        return loop_flag_dic[guild_id]

    @commands.command(aliases=["p"])
    async def plak(self, ctx, *, url):
        global loop_flag_dic
        global setlist_dic
        global now_music
        guild_id = ctx.guild.id
        channel = ctx.author.voice
        if channel is None:
            return await ctx.send("❌You have to be in a voice channel to use this command.")
        else:
            if ctx.voice_client:
                pass
            else:
                loop_flag_dic[guild_id] = False
                setlist_dic[guild_id] = []
                await ctx.author.voice.channel.connect()
                await ctx.send(f":thumbsup: **Joined `{ctx.voice_client.channel.name}` and bound to #{ctx.channel.name}**")

        setlist_dic[guild_id].append(url)
        await ctx.send(f":musical_note: Searching :mag_right: {url}")

        if ctx.voice_client.is_playing():
            pass
        else:
            while 1:
                while ctx.voice_client.is_playing():
                    await asyncio.sleep(0.5)
                if loop_flag_dic[guild_id]:
                    setlist_dic[guild_id].insert(0, now_music[guild_id])
                now_music[guild_id] = setlist_dic[guild_id].pop(0)
                async with ctx.typing():
                    player = await YTDLSource.from_url(now_music[guild_id], loop=self.bot.loop, stream=True)
                    if player.time <3600:
                        player = await YTDLSource.from_url(now_music[guild_id], loop=self.bot.loop)
                    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                await ctx.send('Playing :notes: {} - Now!'.format(player.title))
            await ctx.send(setlist_dic[guild_id])


    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command(aliases=["bye", "dis", "dc"])
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()
        await ctx.send("📭 **Successfully disconnected**")

    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot.add_cog(Music(bot))

@bot.event
async def on_ready():
	print("on_ready")




bot.run(token)