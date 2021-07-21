from discord.ext import commands
import os
import traceback
import discord
import random
from random import randint
import asyncio
import numpy as np
from MakeTeam import MakeTeam
from omikuji_result import omikuji_result

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)
token = os.environ['DISCORD_BOT_TOKEN']
embed = discord.Embed()
embed.color = discord.Color.blue()

batugame = [
    "自身の良いところを熱く語る", "語尾に「にゃん」と言う", "一位の人をご主人様と呼ぶ", "語尾にぴょんと言う",
    "ギルドのメンバーで付き合うなら誰？", "テンションを上げる", "ミッキー口調になる", "恥ずかしいor面白い話",
    "厨二病キャラになる", "メンバー1名を褒める", "一曲歌う", "ギルドの中で嫌いな人は？", "勝者の誰かに嘘告白",
    "陽キャになる", "初恋の人の名前", "グーフィーになる", "アニメのキャラになる", "罰ゲーム回避", "ドナルドのモノマネ",
    "ツンデレになる", "今の気持ちを一句", "語尾にござるを付ける", "フェチを一つ暴露"
]

random_contents = [
	"みょすたのこと呼んだ...？","みょすただよ！！","みょすた参上...!","みょすたって響きいいよね","みょすたは不滅！","みょすたんたんめん","みょすたいやき",
	"みょすたるたるそーす","みょすたっかるび","みょすたこやき","みょすたは食べ物だった...？","みょんみょんみょんみょん",
	"そろそろみょすたると崩壊してきた？","もしもし、私みょすたさん。今あなたの後ろにいるの。","魔法少女みょすた、キミのために戦うよ！","みんなの夢を守るため、みょすた、戦います！",
	"みょすたみんと鬼龍のみょすみんです！しゅび！！","みょすたぴおか","みょすたまごかけごはん","みょすたこす","みょすたこらいす","みょすたいあたり！！","みょすたとお友達になってくれる？",
	"選ばれたのは....みょすたでした！！"
]

character = [
	"アタリ","ジャスティス","リリカ","ノホ","忠臣","ジャンヌ","マルコス","ルチアーノ","voidoll","まとい","ソル","ディズィー","グスタフ","テスラ","ミク",
	"ヴィオレッタ","コクリコ","リュウ","春麗","マリア","アダム","１３","勇者","エミリア","レム","カイ","メグメグ","リン","レン","イスタカ","ザクレイ",
	"きらら","モノクマ","ポロロッチョ","デルミン","トマス","猫宮","オカリン","レイヤ","セイバーオルタ","英雄王ギルガメッシュ","ルルカ","ピエール","佐藤四郎兵衛忠信",
	"アイズ・ヴァレンシュタイン","狐ヶ崎甘色","ノクティス","ニーズヘッグ","中島敦","芥川龍之介","ゲームバズーカガール","リヴァイ"
]

attacker = [
	"ノホ", "忠臣", "マルコス", "ソル＝バッドガイ", "リュウ", "アダム＝ユーリエフ", "レム", "カイ=キスク",
	"リヴァイ", "デビルミント鬼龍　デルミン", "ヴィーナス　ポロロッチョ", "マリア＝s＝レオンブルク",
	"セイバーオルタ", "ルルカ", "アイス・ヴァレンシュタイン", "狐ヶ咲　甘色", "ノクティス",
]

card = [
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



@bot.command()
async def batu(ctx):
    embed.clear_fields()
    hero = random.choice(batugame)
    embed.title = f"{ctx.author.name}"
    embed.description = f"{hero}"
    await ctx.send(embed=embed)

@bot.command()
async def batu_list(ctx):
    word_list = "\n".join(batugame)
    await ctx.send(word_list)



@bot.command()
async def kuji(ctx, num = 1):
    number_list = list(range(int(num)))
    for n in number_list:
        dice = list(range(1, 8))
        kakuritu = np.random.choice(
            dice, p=[0.0000001, 0.0000002, 0.00001, 0.0001, 0.01, 0.1, 0.8898897]
        )
        if kakuritu == 1:
            await ctx.send("1等！５億円！！")
        elif kakuritu == 2:
            await ctx.send("2等！2000万円！！")
        elif kakuritu == 3:
            await ctx.send("3等！100万円！！")
        elif kakuritu == 4:
            await ctx.send("4等！5万円！！")
        elif kakuritu == 5:
            await ctx.send("5等！3000円！！")
        elif kakuritu == 6:
            await ctx.send("6等！300円")
        elif kakuritu == 7:
            await ctx.send("残念！ハズレだよ！")

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
async def omikuji(ctx):
    await ctx.send(omikuji_result())

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

	if message.author == bot.user:
		#botからのメッセージには反応しない
		#この判定をしないと無限ループが起きる
		return

	if "みょすた" in message.content:
		content = random.choice(random_contents)
		await message.channel.send(content)

	await bot.process_commands(message)

@bot.command()
async def slot(ctx):
    kakuritu = random.randint(1, 15)
    slot_list = ['\U00002660', '\U00002663', '\U00002665', '\U00002666', ':seven:']
    A = random.choice(slot_list)
    B = random.choice(slot_list)
    C = random.choice(slot_list)
    if int(kakuritu) == int(1):
        await ctx.send("ボーナス確定！！！")
        await asyncio.sleep(3)
        await ctx.send(':seven: :seven: :seven:')
    else:
        await ctx.send("%s%s%s" % (A, B, C))

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

@bot.command()
async def ahd(ctx):
	if ctx.author.voice is None:
		await ctx.send("vcに入ってないから実行できないよ！！！")
	member = [member.name for member in ctx.author.voice.channel.members]
	menber_num = len(ctx.author.voice.channel.members)
	embed.clear_fields()
	embed.add_field(name="a", value="a")
	for val in member:
		hero = random.choice(character)
		deck = random.choices(card, k=4)
		deck = ('、'.join(deck))
		embed.title = f"{val}"
		embed.description = None
		embed.set_field_at(0,name=f"{hero}", value=deck)
		await ctx.send(embed=embed)

@bot.command()
async def hd(ctx):
	hero = random.choice(character)
	deck = random.choices(card, k=4)
	deck = ('、'.join(deck))
	embed.clear_fields()
	embed.title = f"{ctx.author.name}"
	embed.description = None
	embed.add_field(name=f"{hero}", value=deck)
	await ctx.send(embed=embed)

@bot.command()
async def hero(ctx):
	embed.clear_fields()
	hero = random.choice(character)
	embed.title = f"{ctx.author.name}"
	embed.description = f"{hero}"
	await ctx.send(embed=embed)

@bot.command()
async def deck(ctx):
	embed.clear_fields()
	deck = random.choices(card, k=4)
	deck = ('、'.join(deck))
	embed.title = f"{ctx.author.name}"
	embed.description = f"{deck}"
	await ctx.send(embed=embed)


@bot.command()
async def myosta(ctx):
    embed.clear_fields()
    embed.title = "みょすたbotの使い方"
    embed.add_field(name="/hero", value="ランダムにヒーローを指定するよ")
    embed.add_field(name="/deck", value="ランダムにデッキを指定するよ")
    embed.add_field(name="/hd", value="ランダムにヒーローとデッキを指定するよ")
    embed.add_field(name="/ahd", value="ボイスチャットに入ってる人のデッキとヒーローをランダムに指定するよ")
    embed.add_field(name="/team", value="ボイスチャットに入ってる人をチーム分けしてくれるよ")
    embed.add_field(name="/team_norem", value="基本的には/teamと同じだけど、こっちはあまりが出ないよ")
    embed.add_field(name="/member_info", value="コマンドを打った人の情報を表示するよ")
    embed.add_field(name="/batu", value="みょすたが罰ゲームを考えてくれるよ")
    embed.add_field(name="/batu_list", value="罰ゲーム一覧を表示するよ")
    await ctx.send(embed=embed)



@bot.command()
async def team(ctx, specified_num=2):
    make_team = MakeTeam()
    remainder_flag = 'true'
    msg = make_team.make_party_num(ctx,specified_num,remainder_flag)
    await ctx.channel.send(msg)

@bot.command()
async def team_norem(ctx, specified_num=2):
    make_team = MakeTeam()
    msg = make_team.make_party_num(ctx,specified_num)
    await ctx.channel.send(msg)

@bot.command()
async def group(ctx, specified_num=1):
    make_team = MakeTeam()
    msg = make_team.make_specified_len(ctx,specified_num)
    await ctx.channel.send(msg)

bot.load_extension("cogs.greet")
bot.run(token)