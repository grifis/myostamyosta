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
import urllib.parse
import re

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)
token = os.environ['DISCORD_BOT_TOKEN']
embed = discord.Embed()
embed.color = discord.Color.blue()
lang = os.getenv('DISCORD_BOT_LANG', default='ja')
channel_id = {}

batugame = [
    "自身の良いところを熱く語る", "語尾ににゃんと言う", "一位の人をご主人様と呼ぶ", "語尾にぴょんと言う",
    "ギルドのメンバーで付き合うなら誰？", "テンションを上げる", "ミッキー口調になる", "恥ずかしいor面白い話",
    "厨二病キャラになる", "メンバー1名を褒める", "好きな曲を1フレーズ歌う", "ギルドの中で密かにライバル視してる人を言う", "勝者の誰かに嘘告白",
    "語尾にですわをつける", "初恋の人の名前", "グーフィーになる", "アニメのキャラになる", "罰ゲーム回避", "ドナルドのモノマネ",
    "ツンデレになる", "今の気持ちを一句", "語尾にござるを付ける", "フェチを一つ暴露", "ポロロッチョのモノマネをする",
    "恋人に求める条件を言う", "苦手な教科とその理由", "苦手なスポーツとその理由", "苦手な食べ物とその理由", "理想的なデートのシチュエーションを暴露",
    "今まで付き合った人数を言う", "コンパスヒーローの中で付き合うなら誰？", "テストで取った最低得点", "苦手な生き物とその理由",
    "関西弁で喋る", "博多弁で喋る", "ギルメンに言ってない秘密を暴露", "自分を動物で例えると？", "一位の人の良いところを挙げる",
    "恋愛対象は何歳まで?", "結婚するとしたらいつまでにしたい？", "最近買った一番高いものは？", "人生で一番辛かったことは？", "今までで死にかけたことはある？",
    "一人称を自分の名前にする", "語尾にぴえんをつける", "自慢できることを一つ言う"
]

batugame_kikisen = [
    "自身のいいところを熱く語る", "ギルドのメンバーで付き合うなら誰？", "恥ずかしい話をする", "メンバー1名を褒める", "ギルドの中で密かにライバル視している人をいう",
    "今の気持ちを一句", "恋人に求める条件を言う", "苦手な教科とその理由", "苦手なスポーツとその理由", "苦手な食べ物とその理由", "理想的なデートのシチュエーション",
    "今まで付き合った人数を言う", "苦手な教科とその理由", "苦手なスポーツとその理由", "苦手な食べ物とその理由", "理想的なデートのシチュエーションを暴露",
    "コンパスヒーローで付き合うなら誰？", "テストで撮った最低得点", "苦手な生き物とその理由", "ギルメンに言ってない秘密を暴露", "自分を動物で例えると？",
    "一位の人のいいところを挙げる", "恋愛対象は何歳まで？", "結婚するとしたらいつまでにしたい？", "最近買った一番高いものは？", "人生で一番辛かったことは？",
    "今までで死にかけたことはある？", "好きな異性の髪型は？", "自慢できることを一つ言う"
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
	"アイズ・ヴァレンシュタイン","狐ヶ崎甘色","ノクティス","ニーズヘッグ","中島敦","芥川龍之介","ゲームバズーカガール","リヴァイ","ライザリン・シュタウト","青春アリス",
    "ジョーカー","イグニス＝ウィル＝ウィスプ","アインズ・ウール・ゴウン", "糸廻 輪廻","キリト","アスナ","Bugdoll","ステリア・ララ・シルワ","ラム","2B","ラヴィ・シュシュマルシュ",
    "リムル=テンペスト","アル・ダハブ=アルカティア","御坂 美琴","アクセラレータ","天空王 ぶれいずどらごん"
]

attacker = [
	"ノホ", "忠臣", "マルコス", "ソル＝バッドガイ", "リュウ", "アダム＝ユーリエフ", "レム", "カイ=キスク",
	"リヴァイ", "デビルミント鬼龍　デルミン", "ヴィーナス　ポロロッチョ", "マリア＝s＝レオンブルク",
	"セイバーオルタ", "ルルカ", "アイス・ヴァレンシュタイン", "狐ヶ咲　甘色", "ノクティス",
]

card = [
	"近距離","遠距離","連続","周囲","回復","ガード","強化","弱体化","移動","設置","その他"
]

custum_list = [
    "『攻撃あるのみ』\nこのバトルでは【近】【遠】【周】【連】のカードのみを使うことができます。回復（始龍系含む）やダメージカット等、その他のカードは一切使用禁止です。",
    "『attacker's party』\nこのバトルはアタッカーのみで行われます。カードは自由に積むことができます。",
    "『gunner's party』\nこのバトルではガンナーのみで行われます。カードは自由に積むことができます。",
    "『gunner's party』\nこのバトルではガンナーのみで行われます。カードは自由に積むことができます。",
    "『sprinter's party』\nこのバトルではスプリンターのみで行われます。カードは自由に積むことができます。",
    "『tank's party』\nこのバトルではタンクのみで行われます。カードは自由に積むことができます。",
    "『minesweeper』\nこのバトルでは【設置】カード（罠カード）を３枚以上積まなければいけません。残りの1枠に関しては自由です。",
    "『LOSER's』\nこのバトルでは勝率最下位のキャラクターor使用したことがないキャラクターのみ使えます。カードは自由です。勝率の見方は「バトル」⇨「個人ヒーローランキング」→「勝率」を選択することで見れます。",
    "『BERSERKER's』\nこのバトルでは キル数一位のキャラクターのみ使えます。カードは自由です。キル数の見方は「バトル」⇨「個人ヒーローランキング」→「キル数」を選択することで見れます。",
    "『毒の海』\nこのバトルでは「毒」効果のあるカードを２枚以上入れてください。残り２枠は自由、キャラクターも自由です。",
    "『ビリビリ！?スタン地獄』\nこのバトルでは「スタン」効果のあるカードを２枚以上入れてください。残り２枠は自由、キャラクターはカイ＝キスクのみ禁止です。",
    "『お前今煽ったな？ぜってぇぶっ殺す！！』\nこのバトルでは敵をキルした後は必ずアピールをしてください。たとえ他の敵が残っていたとしても強制的にアピールをしなくてはなりません。また、アピールで煽るのは結構ですが、チャット、ボイスチャットで煽るのは控えてください。リアルファイトになってもギルマスは責任を取りません（）",
    "『あべこべ！鏡の国のコンパス』\nこのバトルでは端末を逆さに持ってプレイしてください。それ以外のルールは特にありません。",
    "『くっ...俺の腕が疼くぜ....』\nこのバトルでは両腕を使ってプレイするのは禁止です。片腕で頑張ってプレイしてください",
    "『Time alter ---- double accel』\nこのバトルはゲームスピード倍率を2倍にし、試合時間を300秒にして行います。",
    "『蒼紅聖戦』\nこのバトルではアダム、もしくはマリアのみを使用することができます。",
    "『夢を力に　愛を届けに!』\nこのバトルではリリカ、ルルカ、マルコスのみを使用することができます。",
    "『トリガーハッピー』\nこのバトルでは銃を用いて攻撃するキャラのみを使用することができます。",
    "『ドキッ！凍死だらけの氷柱大会！』\nこのバトルはアダムのみを使用することができ、攻撃倍率5倍、防御倍率0.5倍、ライフ倍率0.5で行われます。攻撃はHA(氷柱タメ攻撃)のみ、カード、通常攻撃は禁止です。"
]

list_vote = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

another_games = ['God Field', 'お絵描きしりとり', '大富豪', 'みんなで早押しクイズ']

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.event
async def on_ready():
	print("on_ready")

@bot.command()
async def 別ゲー(ctx):
    embed = discord.Embed(title='遊びたいゲームにリアクションをしてね♪', description="", color=discord.Color.green())
    for i in range(len(another_games)):
        embed.description = embed.description + list_vote[i] + "  " + another_games[i] + "\n"

    voting_msg = await ctx.send(embed=embed)
    for i in range(len(another_games)):
        await voting_msg.add_reaction(list_vote[i])
    return

@bot.command(aliases=['c'])
async def cus(ctx):
    rule = random.choice(custum_list)
    await ctx.send(rule)

@bot.command()
async def batu(ctx):
    if ctx.author.voice:
        if ctx.author.voice.self_mute:
            embed.clear_fields()
            hero = random.choice(batugame_kikisen)
            embed.title = f"{ctx.author.name}"
            embed.description = f"{hero}"
            await ctx.send(embed=embed)
        else:
            embed.clear_fields()
            hero = random.choice(batugame)
            embed.title = f"{ctx.author.name}"
            embed.description = f"{hero}"
            await ctx.send(embed=embed)
    else:
        await ctx.send("ボイスチャンネルに入ってからコマンドを打ってね")

@bot.command()
async def batu_list(ctx):
    word_list = "\n".join(batugame)
    await ctx.send(word_list)



@bot.command()
async def 宝くじ(ctx, num = 1):
    number_list = list(range(int(num)))
    result = []
    for n in number_list:
        dice = list(range(1, 8))
        kakuritu = np.random.choice(
            dice, p=[0.0000001, 0.0000002, 0.00001, 0.0001, 0.01, 0.1, 0.8898897]
        )
        if kakuritu == 1:
            result.append("1等！５億円！！")
        elif kakuritu == 2:
            result.append("2等！2000万円！！")
        elif kakuritu == 3:
            result.append("3等！100万円！！")
        elif kakuritu == 4:
            result.append("4等！5万円！！")
        elif kakuritu == 5:
            result.append("5等！3000円！！")
        elif kakuritu == 6:
            result.append("6等！300円")
        elif kakuritu == 7:
            result.append("残念！ハズレだよ！")
    content = "\n".join(result)
    await ctx.send(content)

def hand_to_int(hand):
    """
    グー: 0, チョキ: 1, パー: 2 とする
    handはカタカナ，ひらがな表記，数字に対応する
    """
    hand_int = None
    if hand in ["グー", "ぐー", "goo", "ぐ", "0"]:
        hand_int = 0
    elif hand in ["チョキ", "ちょき", "1", "choki"]:
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
    embed.add_field(name="/宝くじ 10", value="宝くじを10枚買えるよ")
    embed.add_field(name="/hero", value="ランダムにヒーローを指定するよ")
    embed.add_field(name="/deck", value="ランダムにデッキを指定するよ")
    embed.add_field(name="/hd", value="ランダムにヒーローとデッキを指定するよ")
    embed.add_field(name="/ahd", value="ボイスチャットに入ってる人のデッキとヒーローをランダムに指定するよ")
    embed.add_field(name="/team", value="ボイスチャットに入ってる人をチーム分けしてくれるよ")
    embed.add_field(name="/team_norem", value="基本的には/teamと同じだけど、こっちはあまりが出ないよ")
    embed.add_field(name="/member_info", value="コマンドを打った人の情報を表示するよ")
    embed.add_field(name="/batu", value="みょすたが罰ゲームを考えてくれるよ")
    embed.add_field(name="/batu_list", value="罰ゲーム一覧を表示するよ")
    embed.add_field(name="/s", value="みょすたが読み上げをしてくれます")
    embed.add_field(name="/dc", value="みょすたが読み上げを終了します")
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


@bot.command()
async def s(ctx):
    global channel_id
    guild_id = ctx.guild.id
    channel_id[guild_id] = ctx.channel.id
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
async def dc(ctx):
    if ctx.message.guild:
        if ctx.voice_client is None:
            await ctx.send('ボイスチャンネルに接続していません。')
        else:
            await ctx.voice_client.disconnect()


@bot.event
async def on_message(message):
    guild_id = message.guild.id
    if message.channel.id == channel_id.get(guild_id):
        if message.content.startswith("$"):
            pass
        else:
            if message.guild.voice_client:
                text = message.content
                text = text.replace('\n', '、')
                pattern = r'<@(\d+)>'
                match = re.findall(pattern, text)
                for user_id in match:
                    user = await bot.fetch_user(user_id)
                    username = f'、{user.name}へのメンション、'
                    text = re.sub(f'<@{user_id}>', username, text)
                pattern = r'<@&(\d+)>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    emoji_read_name = emoji_name.replace('_', ' ')
                    text = re.sub(rf'<:{emoji_name}:\d+>', f'、{emoji_read_name}、', text)
                pattern = r'<:emoji_9:936968342823112705>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:emoji_9:936968342823112705>', f'じもいわぁぁぁ、', text)

                pattern = r'<:niko:936098021085700096>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:niko:936098021085700096>', f'ぴえん', text)

                pattern = r'<:emoji_3:1077879495245189160>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:emoji_3:1077879495245189160>', f'解散！！', text)

                pattern = r'<:emoji_13:936968454865584149>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:emoji_13:936968454865584149>', f'固定いく?', text)

                pattern = r'<:age:936968361504571462>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:age:936968361504571462>', f'ワラ', text)

                pattern = r'<:emoji_8:936968294278250606>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:emoji_8:936968294278250606>', f'プンスカ', text)

                pattern = r'<:agekappa:956543816050028574>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:agekappa:956543816050028574>', f'アゲカッパ', text)

                pattern = r'<:emoji_4:936098759937491045>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:emoji_4:936098759937491045>', f'にっこぉぉ', text)

                pattern = r'<:emoji_6:936968255246053406>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:emoji_6:936968255246053406>', f'紅茶いれてくる！', text)

                pattern = r'<:ha:936092299056775189>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:ha:936092299056775189>', f'はぁぁ？、', text)

                pattern = r'<:emoji_5:936968239399972964>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:emoji_5:936968239399972964>', f'おい！！、', text)

                pattern = r'<:emoji_7:936968271377342474>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:emoji_7:936968271377342474>', f'じゃがん', text)

                pattern = r'<:emoji_14:957262262798782555>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:emoji_14:957262262798782555>', f'スプをちょうだいいたす', text)

                pattern = r'<:emoji_17:958029223958839297>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:emoji_17:958029223958839297>', f'部屋はり', text)

                pattern = r'<:[a-zA-Z0-9_]+:[0-9]+>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    text = re.sub(rf'<:[a-zA-Z0-9_]+:[0-9]+>', f'、あげさん、', text)
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
            presence = f'{len(bot.voice_clients)}/{len(bot.guilds)}サーバー'
            await bot.change_presence(activity=discord.Game(name=presence))
        else:
            if member.guild.voice_client is None:
                pass
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
            presence = f'{len(bot.voice_clients)}/{len(bot.guilds)}サーバー'
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


bot.load_extension("cogs.notify")
bot.load_extension("cogs.greet")
bot.run(token)
