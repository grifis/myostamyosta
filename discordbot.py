from discord.ext import commands
import os
import traceback
import discord
import random

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

random_contents = [
	"みょすたのこと呼んだ...？",
	"みょすただよ！！",
	"みょすた参上...!",
	"みょすたって響きいいよね",
	"みょすたは不滅！",
	"みょすたんたんめん",
	"みょすたいやき",
	"みょすたるたるそーす",
	"みょすたっかるび",
	"みょすたこやき",
	"みょすたは食べ物だった...？",
	"みょんみょんみょんみょん",
	"そろそろみょすたると崩壊してきた？"
]

character = [
	"アタリ",
	"ジャスティス",
	"リリカ",
	"ノホ",
	"忠臣",
	"ジャンヌ",
	"マルコス",
	"ルチアーノ",
	"voidoll",
	"まとい",
	"ソル",
	"ディズィー",
	"グスタフ",
	"テスラ",
	"ミク",
	"ヴィオレッタ",
	"コクリコ",
	"リュウ",
	"春麗",
	"マリア",
	"アダム",
	"１３",
	"勇者",
	"エミリア",
	"レム",
	"カイ",
	"メグメグ",
	"リン",
	"レン",
	"イスタカ",
	"ザクレイ",
	"きらら",
	"モノクマ",
	"ポロロッチョ",
	"デルミン",
	"トマス",
	"猫宮",
	"オカリン",
	"レイヤ",
	"セイバーオルタ",
	"ギルガメッシュ",
	"ルルカ",
	"ピエール",
	"佐藤四郎兵衛忠信",
	"アイズ",
	"狐ヶ崎甘色",
	"ノクティス",
	"ニーズヘッグ",
	"中島敦",
	"芥川龍之介",
	"ゲームバズーカガール"
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

	if "ランダムヒーローデッキ" in message.content:
		deck_a = random.sample(deck,4)
		hero = random.choice(character)
		dh = print(hero, deck_a)
		await message.channel.send(dh)

	await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run(token)
