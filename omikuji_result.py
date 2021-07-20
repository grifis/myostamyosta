import random

def omikuji_result():
    num = random.randint(0,600)

    if num < 20:
        return "大吉"
    elif 20 <= num < 100:
        return "中吉"
    elif 100 <= num < 200:
        return "小吉"
    elif 200 <= num < 400:
        return "吉"
    elif 400 <= num < 500:
        return "末吉"
    elif 500 <= num < 550:
        return "凶"
    elif 550 <= num < 580:
        return "中凶"
    elif 580 <= num < 581:
        return "超大吉だよ！おめでとう！確率はなんと0.17%だよ！"
    else:
        return "大凶"