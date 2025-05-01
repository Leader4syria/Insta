import requests
import random
from user_agent import generate_user_agent
import os
import time
from cfonts import render
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

# ألوان
B = "\033[0;30m"
R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B_LIGHT = "\033[1;34m"
M = "\033[1;35m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"
RESET = "\033[0m"
CYAN = '\033[1;36m'
WHITE = '\033[1;37m'
GRAY = '\033[1;90m'
ORANGE = '\033[38;5;208m'

# تنظيف الشاشة
os.system('clear')


tok = '7637224269:AAG98CSXSAvyPb3sjBkLCXnekfzce0D_Bxs'
id = '7721705352'

import random

import random

def generate_username(length=5):
    if length != 5:
        raise ValueError("الطول يجب أن يكون 5 بالضبط حسب الشروط.")

    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    symbols = ['_', '.']

    while True:
        username_chars = []

        # اختر الحرف المتكرر 3 مرات
        repeat_char = random.choice(chars)
        username_chars += [repeat_char] * 3

        # أضف رمزين: أحدهما على الأقل نقطة
        chosen_symbols = random.choices(symbols, k=2)
        username_chars += chosen_symbols

        # خلط الأحرف
        random.shuffle(username_chars)

        # تحقق من أن النقطة ليست في البداية أو النهاية
        if username_chars[0] == '.' or username_chars[-1] == '.':
            continue  # أعد التوليد

        username = ''.join(username_chars)
        return username

def check_username():
    try:
        user = generate_username(5)
        time.sleep(0.3)

        cookies = {
            'csrftoken': 'Eh7x9pdsijAlrKUv_2By8c',
            'datr': '8tDyZ1KMWhz6FUOf2XKRajCF',
            'ig_did': 'FC65D64D-5D35-4EE5-9019-8F272039731F',
            'mid': 'Z_LQ8gABAAEg4fpyKTNdFBvFflrm',
            'dpr': '2.5964407920837402',
            'ig_nrcb': '1',
            'ps_l': '1',
            'ps_n': '1',
            'wd': '990x945',
        }

        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'ar',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/emailsignup/',
            'user-agent': generate_user_agent(),
            'x-csrftoken': 'Eh7x9pdsijAlrKUv_2By8c',
            'x-ig-app-id': '936619743392459',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'email': '',
            'first_name': '',
            'username': user,
            'opt_into_one_tap': 'false',
            'use_new_suggested_user_name': 'true',
            'jazoest': '21995',
        }

        res = requests.post(
            'https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/',
            cookies=cookies,
            headers=headers,
            data=data
        )

        result = res.json()
        if result.get("errors", {}).get("username"):
            print(f'{BOLD}{R}🜲  𝐁𝐀𝐃 𝐔𝐒𝐄𝐑 | {user}')
        else:
            print(f'{BOLD}{G}🜲  𝐆𝐎𝐎𝐃 𝐔𝐒𝐄𝐑 | {user}')

            use = f"""
┏━━━━━━━━━━━━━━━┓
┃ ✅ 𝐔𝐒𝐄𝐑 𝐂𝐋𝐀𝐈𝐌𝐄𝐃        ┃
┗━━━━━━━━━━━━━━━┛
• 𝗣𝗟𝗔𝗧𝗙𝗢𝗥𝗠 : INSTA  
• 𝗨𝗦𝗘𝗥 : `{user}`  
• 𝗖𝗢𝗗𝗘𝗗 𝗕𝗬 : @SYRIA7R  
"""

            response = requests.get(
                f"https://api.telegram.org/bot{tok}/sendMessage",
                params={
                    "chat_id": id,
                    "text": use,
                    "parse_mode": "Markdown"
                }
            )

    except Exception as e:
        print(f'{R}[ERROR] {e}')

# بدء التنفيذ بخيوط متعددة
with ThreadPoolExecutor(max_workers=30) as executor:
    while True:
        executor.submit(check_username)