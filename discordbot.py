from discord.ext import commands
import os
import traceback
import discord
import random
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

random_contents = [
	"みょすたのこと呼んだ...？",　"みょすただよ！！",　"みょすた参上...!","みょすたって響きいいよね",
	"みょすたは不滅！","みょすたんたんめん","みょすたいやき",
	"みょすたるたるそーす",　"みょすたっかるび"
	"みょすたこやき",
	"みょすたは食べ物だった...？",
	"みょんみょんみょんみょん",
	"そろそろみょすたると崩壊してきた？"
]

character = [
	"アタリ",　"ジャスティス",　"リリカ",　"ノホ",　"忠臣",　"ジャンヌ",　"マルコス",　"ルチアーノ",　"voidoll",　"まとい",　"ソル",　"ディズィー",　"グスタフ",　"テスラ",　"ミク",
	"ヴィオレッタ",　"コクリコ",　"リュウ",　"春麗",　"マリア",　"アダム",　"１３",　"勇者",　"エミリア",　"レム",　"カイ",　"メグメグ",　"リン",　"レン",　"イスタカ",　"ザクレイ",
	"きらら",　"モノクマ",　"ポロロッチョ",　"デルミン",　"トマス",　"猫宮",　"オカリン",　"レイヤ",　"セイバーオルタ",　"ギルガメッシュ",　"ルルカ",　"ピエール",　"佐藤四郎兵衛忠信",
	"アイズ",　"狐ヶ崎甘色",　"ノクティス",　"ニーズヘッグ",　"中島敦",　"芥川龍之介",　"ゲームバズーカガール"
]

attacker = [
	"ノホ", "忠臣", "マルコス", "ソル＝バッドガイ", "リュウ", "アダム＝ユーリエフ", "レム", "カイ=キスク", 
	"リヴァイ", "デビルミント鬼龍　デルミン", "ヴィーナス　ポロロッチョ", "マリア＝s＝レオンブルク",
	"セイバーオルタ", "ルルカ", "アイス・ヴァレンシュタイン", "狐ヶ咲　甘色", "ノクティス",
]

deck = [
	"近距離", "遠距離", "連続", "周囲", "回復", "ガード", "強化", "弱体化", "移動", "設置", "その他"
]


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.event
async def on_ready():
	print("on_ready")

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.event
async def on_message(message):


	msgclient = message.guild.voice_client

	if message.guild.voice_client:
		print(message.content)
		creat_WAV(message.content)
		source = discord.FFmpegPCMAudio("output.wav")
		message.guild.voice_client.play(source)

	if message.author == bot.user:
		#botからのメッセージには反応しない
		#この判定をしないと無限ループが起きる
		return

	if "みょすた" in message.content:
		content = random.choice(random_contents)
		await message.channel.send(content)


	if "ダイキュリー" in message.content:
		await message.channel.send("ダイキュリーアイス")

	if "ランダムヒーロー" in message.content:
		hero = random.choice(character)
		await message.channel.send(hero)

	if "ランダムアタッカー" in message.content:
		hero_a = random.choice(attacker)
		await message.channel.send(hero_a)

	if "ランダムデッキ" in message.content:
		deck_a = random.choices(deck, k=4)
		await message.channel.send(deck_a)

	if "ヒーローデッキ" in message.content:
		def random_hero:
			a = random.sample(deck,4)
			b = random.choice(character)
			c = print(a + b)
			return c
		
		await message.channel.send(random_hero)
		

	await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def hello(ctx):
	def check_message_author(msg):
		return msg.author == ctx.author

	await ctx.send(f"こんにちは、{ctx.author.name}さん！！")
	await ctx.send("気分はどうかな？")

	msg = await bot.wait_for('message' , check=check_message_author)
	await ctx.send(f" 「{msg.content}」という気分なんだね！！！")

@bot.command()
async def cha(ctx):
	content = random.choice(character)
	await ctx.send(content)

@bot.command()
async def vc(ctx):
	member = ctx.author
	if member.voice and member.voice.channel:
		await ctx.send(f"{ctx.author.name}は「{member.voice.channel.name}」にいるよ！")
	else:
		await ctx.send(f"あなたはボイスチャンネルに参加してないよ！！")

@bot.command()
async def move(ctx, member: discord.Member,
	voice_channel:discord.VoiceChannel):
	if not member.voice or not member.voice.channel:
		await ctx.send("ボイスチャンネルに参加してないよ。")
		return
	await member.move_to(voice_channel)
	await ctx.send(
		f"{member.name}をボイスチャンネル{voice_channel.name}に移動したよ！")
	
@bot.command()
async def message(ctx, member:discord.Member, content):
	await ctx.send(f"{member.name}にDMを送信するよ。")
	await member.send(content=content)

@bot.command()
async def member_info(ctx):
	from datetime import timedelta
	member = ctx.author
	await ctx.send(
		f"ユーザー名:{member.name}\n"
		f"ユーザーID:{member.id}\n"
		f"Discordを始めた日:{member.created_at + timedelta(hours=9)}\n"
		f"Guildへの参加日:{member.joined_at + timedelta(hours=9)}\n"
		f"ステータス:{str(member.status)}\n"
		f"モバイルからのログイン？:{member.is_on_mobile()}" 
		)

@tasks.loop(seconds=5.0)
async def notifier(self):
	print("start_notifier")
	now = datetime.now()
	if self.channel:
		await self.channel.send(
			f"現在、{now.strftime('%Y/%m/%d %H:%M:%S')}です")

bot.run(token)
