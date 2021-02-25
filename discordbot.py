from discord.ext import commands
import os
import traceback
import discord
import random
from random import randint

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


random_contents = [
	"みょすたのこと呼んだ...？",
	"みょすただよ！！",
	"みょすた参上...!",
	"みょすたって響きいいよね",
	"みょすたは不滅！","みょすたんたんめん","みょすたいやき",
	"みょすたるたるそーす","みょすたっかるび",
	"みょすたこやき",
	"みょすたは食べ物だった...？",
	"みょんみょんみょんみょん",
	"そろそろみょすたると崩壊してきた？","もしもし、私みょすたさん。今あなたの後ろにいるの。"
]

character = [
	"アタリ","ジャスティス","リリカ","ノホ","忠臣","ジャンヌ","マルコス","ルチアーノ","voidoll","まとい","ソル","ディズィー","グスタフ","テスラ","ミク",
	"ヴィオレッタ","コクリコ","リュウ","春麗","マリア","アダム","１３","勇者","エミリア","レム","カイ","メグメグ","リン","レン","イスタカ","ザクレイ",
	"きらら","モノクマ","ポロロッチョ","デルミン","トマス","猫宮","オカリン","レイヤ","セイバーオルタ","英雄王ギルガメッシュ","ルルカ","ピエール","佐藤四郎兵衛忠信",
	"アイズ・ヴァレンシュタイン","狐ヶ崎甘色","ノクティス","ニーズヘッグ","中島敦","芥川龍之介","ゲームバズーカガール"
]

attacker = [
	"ノホ", "忠臣", "マルコス", "ソル＝バッドガイ", "リュウ", "アダム＝ユーリエフ", "レム", "カイ=キスク", 
	"リヴァイ", "デビルミント鬼龍　デルミン", "ヴィーナス　ポロロッチョ", "マリア＝s＝レオンブルク",
	"セイバーオルタ", "ルルカ", "アイス・ヴァレンシュタイン", "狐ヶ咲　甘色", "ノクティス",
]

deck = [
	"近距離","遠距離","連続","周囲","回復","ガード","強化","弱体化","移動","設置","その他"
]


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.event
async def on_ready():
	print("on_ready")


def hand_to_int(hand):
    """
    グー: 0, チョキ: 1, パー: 2 とする
    handはカタカナ，ひらがな表記，数字に対応する
    """
    hand_int = None
    if hand in ["グー", "ぐー", "0"]:
        hand_int = 0
    elif hand in ["チョキ", "ちょき", "1"]:
        hand_int = 1
    elif hand in ["パー", "ぱー", "2"]:
        hand_int = 2

    return hand_int


def get_player_result(player_hand, bot_hand):
    """
    勝利: 1, 敗北: 0, ひきわけ: 2 とする
    result_table[player_hand][bot_hand]で結果がわかるようにする
    """
    result_table = [
        [2, 1, 0],
        [0, 2, 1],
        [1, 0, 2]
    ]
    return result_table[player_hand][bot_hand]


@bot.command()
async def jyanken(ctx, hand):
    hand_emoji_list = [":fist:", ":v:", ":hand_splayed:"]

    player_hand = hand_to_int(hand)
    if player_hand is None:
        await ctx.send("ずるはしちゃダメだよ！もう一度やり直してください！！")
        return

    bot_hand = randint(0, 2)

    await ctx.send(
        f"あなた: {hand_emoji_list[player_hand]}\n"
        f"Bot: {hand_emoji_list[bot_hand]}"
    )

    result = get_player_result(player_hand, bot_hand)
    if result == 0:
        await ctx.send("YOU LOSE  私の勝ち。なんで負けたか明日まで考えておいてください。そしたら何かが見えてくるはずです。ほな頂きます。")
    elif result == 1:
        await ctx.send("おめでとう！君の勝ちだよ！！:tada:")
    else:
        await ctx.send("あいこ！")

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
		hero = random.choice(character)
		deck_a = random.choices(deck, k=4)
		await message.channel.send(hero)
		await message.channel.send(deck_a)
		

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
	await ctx.send("{ctx.author.name}さんは{content}を使ってね！")

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



bot.run(token)
