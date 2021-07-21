import asyncio
import discord
from discord.ext import commands
import os
import traceback
import urllib.parse
import re

prefix = os.getenv('DISCORD_BOT_PREFIX', default='$')
lang = os.getenv('DISCORD_BOT_LANG', default='ja')
bot = commands.Bot(command_prefix=prefix)
token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_ready():
    presence = f'{prefix}ヘルプ | 0/{len(bot.guilds)}サーバー'
    await bot.change_presence(activity=discord.Game(name=presence))

@bot.event
async def on_guild_join(guild):
    presence = f'{prefix}ヘルプ | {len(bot.voice_clients)}/{len(bot.guilds)}サーバー'
    await bot.change_presence(activity=discord.Game(name=presence))

@bot.event
async def on_guild_remove(guild):
    presence = f'{prefix}ヘルプ | {len(bot.voice_clients)}/{len(bot.guilds)}サーバー'
    await client.change_presence(activity=discord.Game(name=presence))

@bot.command()
async def 接続(ctx):
    if ctx.message.guild:
        if ctx.author.voice is None:
            await ctx.send('ボイスチャンネルに接続してから呼び出してください。')
        else:
            if ctx.guild.voice_client:
                if ctx.author.voice.channel == ctx.guild.voice_client.channel:
                    await ctx.send('接続済みです。')
                else:
                    await ctx.voice_client.disconnect()
                    await asyncio.sleep(0.5)
                    await ctx.author.voice.channel.connect()
            else:
                await ctx.author.voice.channel.connect()

@bot.command()
async def 切断(ctx):
    if ctx.message.guild:
        if ctx.voice_client is None:
            await ctx.send('ボイスチャンネルに接続していません。')
        else:
            await ctx.voice_client.disconnect()

@bot.event
async def on_message(message):
    if message.content.startswith(prefix):
        pass
    else:
        if message.guild.voice_client:
            text = message.content
            text = text.replace('\n', '、')
            pattern = r' ?<@(\d+)> '
            match = re.findall(pattern, text)
            for user_id in match:
                user = await bot.fetch_user(user_id)
                username = f'、{user.name}へのメンション、'
                text = re.sub(f' ?<@{user_id}> ', username, text)
            pattern = r'<:([a-zA-Z0-9_]+):\d+>'
            match = re.findall(pattern, text)
            for emoji_name in match:
                emoji_read_name = emoji_name.replace('_', ' ')
                text = re.sub(rf'<:{emoji_name}:\d+>', f'、{emoji_read_name}、', text)
            pattern = r'https://tenor.com/view/[\w/:%#\$&\?\(\)~\.=\+\-]+'
            text = re.sub(pattern, '画像', text)
            pattern = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
            text = re.sub(pattern, '、画像', text)
            pattern = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
            text = re.sub(pattern, '、URL', text)
            text =  text
            if text[-1:] == 'w' or text[-1:] == 'W' or text[-1:] == 'ｗ' or text[-1:] == 'W':
                while text[-2:-1] == 'w' or text[-2:-1] == 'W' or text[-2:-1] == 'ｗ' or text[-2:-1] == 'W':
                    text = text[:-1]
                text = text[:-1] + '、ワラ'
            if message.attachments:
                text += '、添付ファイル'
            if len(text) < 100:
                s_quote = urllib.parse.quote(text)
                mp3url = f'http://translate.google.com/translate_tts?ie=UTF-8&q={s_quote}&tl={lang}&client=tw-ob'
                while message.guild.voice_client.is_playing():
                    await asyncio.sleep(0.5)
                message.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
            else:
                await message.channel.send('100文字以上は読み上げできません。')
        else:
            pass
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:
        if member.id == bot.user.id:
            presence = f'{prefix}ヘルプ | {len(bot.voice_clients)}/{len(bot.guilds)}サーバー'
            await bot.change_presence(activity=discord.Game(name=presence))
        else:
            if member.guild.voice_client is None:
                await asyncio.sleep(0.5)
                await after.channel.connect()
            else:
                if member.guild.voice_client.channel is after.channel:
                    text = member.name + 'さんが入室しました'
                    s_quote = urllib.parse.quote(text)
                    mp3url = f'http://translate.google.com/translate_tts?ie=UTF-8&q={s_quote}&tl={lang}&client=tw-ob'
                    while member.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    member.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
    elif after.channel is None:
        if member.id == bot.user.id:
            presence = f'{prefix}ヘルプ | {len(bot.voice_clients)}/{len(bot.guilds)}サーバー'
            await bot.change_presence(activity=discord.Game(name=presence))
            await bot.change_presence(activity=discord.Game(name=presence))
        else:
            if member.guild.voice_client.channel is before.channel:
                if len(member.guild.voice_client.channel.members) == 1:
                    await asyncio.sleep(0.5)
                    await member.guild.voice_client.disconnect()
                else:
                    text = member.name + 'さんが退室しました'
                    s_quote = urllib.parse.quote(text)
                    mp3url = f'http://translate.google.com/translate_tts?ie=UTF-8&q={s_quote}&tl={lang}&client=tw-ob'
                    while member.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    member.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
    elif before.channel != after.channel:
        if member.guild.voice_client.channel is before.channel:
            if len(member.guild.voice_client.channel.members) == 1 or member.voice.self_mute:
                await asyncio.sleep(0.5)
                await member.guild.voice_client.disconnect()
                await asyncio.sleep(0.5)
                await after.channel.connect()

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, 'original', error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ヘルプ(ctx):
    message = f'''◆◇◆{bot.user.name}の使い方◆◇◆
{prefix}＋コマンドで命令できます。
{prefix}接続：ボイスチャンネルに接続します。
{prefix}切断：ボイスチャンネルから切断します。'''
    await ctx.send(message)

bot.run("NzYzNDI0NDE0ODUwNjEzMjQ5.X33gZA.M9HR_KZDNKcoK0kHfO5gi1_DXWY")