#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, urllib, requests, json, re, os, redis as r
from telebot import types, util, TeleBot
from telebot.apihelper import ApiException
from termcolor import colored
from threading import Timer
from khayyam import JalaliDatetime
reload(sys)
sys.setdefaultencoding("utf-8")
# ----------------------------------------------------- #
redis = r.StrictRedis(host='localhost', port=6379, db=0)
# ----------------------------------------------------- #
channel = -1001474634906
admins = [628547880]
token = "752573563:AAGpyjfc3RI79gaPbPSTF7pSV6UivRsHszs"
bot = TeleBot(token)
# ----------------------------------------------------- #
def is_admin(user):
 var = False
 if user in admins:
  var = True
 return var
# ----------------------------------------------------- #
def set_allowed_(chat, user):
 hash = "{}:alloweds".format(chat)
 redis.sadd(hash, user)
# ----------------------------------------------------- #
def is_allowed(chat, user):
 var = False
 hash = "{}:alloweds".format(chat)
 if redis.sismember(hash, user):
  var = True
 return var
# ----------------------------------------------------- #
def set_allowed(chat, user):
 hash = "{}:alloweds".format(chat)
 if redis.sismember(hash, user):
  return "کاربر {} از قبل در لیست مجاز بود.".format(user)
 else:
  redis.sadd(hash, user)
  return "کاربر {} به لیست مجاز افزوده گردید.".format(user)
# ----------------------------------------------------- #
def rem_allowed(chat, user):
 hash = "{}:alloweds".format(chat)
 if redis.sismember(hash, user):
  redis.srem(hash, user)
  return "کاربر {} از لیست مجاز حذف گردید.".format(user)
 else:
  return "کاربر {} در لیست مجاز نیست.".format(user)
# ----------------------------------------------------- #
def get_num(chat):
 if redis.get("{}:max:adds".format(chat)):
  num = int(redis.get("{}:max:adds".format(chat)))
 else:
  num = 1
 return num
# ----------------------------------------------------- #
def set_num(chat, v):
 hash = "{}:max:adds".format(chat)
 redis.set(hash, v)
# ----------------------------------------------------- #
def get_time(chat):
 if redis.get("{}:del:time".format(chat)):
  num = int(redis.get("{}:del:time".format(chat)))
 else:
  num = 3
 return num
# ----------------------------------------------------- #
def set_time(chat, v):
 hash = "{}:del:time".format(chat)
 redis.set(hash, v)
# ----------------------------------------------------- #
def get_status(chat):
 var = False
 if redis.get("bot:on:{}".format(chat)):
  var = True
 return var
# ----------------------------------------------------- #
def set_status(chat):
 hash = "bot:on:{}".format(chat)
 if redis.get(hash):
  redis.delete(hash)
 else:
  redis.set(hash, True)
# ----------------------------------------------------- #
def get_bots(chat):
 var = False
 if redis.get("bots:add:{}".format(chat)):
  var = True
 return var
# ----------------------------------------------------- #
def set_bots(chat):
 hash = "bots:add:{}".format(chat)
 if redis.get(hash):
  redis.delete(hash)
 else:
  redis.set(hash, True)
# ----------------------------------------------------- #
def get_title(chat_id):
 try:
  chat = bot.get_chat(chat_id)
  return chat.title
 except ApiException as e:
  return '-'
# ----------------------------------------------------- #
def main_gp(chat):
 if get_status(chat):
  status = "✅"
 else:
  status = "❌"
 if get_bots(chat):
  bots = "✅"
 else:
  bots = "❌"
 num = get_num(chat)
 time = get_time(chat)
 mk = types.InlineKeyboardMarkup()
 mk.add(types.InlineKeyboardButton("👥لیست افراد مجاز گروه", callback_data="alloweds_list:{}".format(chat)))
 mk.add(types.InlineKeyboardButton("🤖فعالیت ربات در گروه", callback_data="c"),types.InlineKeyboardButton(status, callback_data="status:{}".format(chat)))
 mk.add(types.InlineKeyboardButton("🔎دسترسی افزودن ربات", callback_data="d"),types.InlineKeyboardButton(bots, callback_data="bots:{}".format(chat)))
 mk.add(types.InlineKeyboardButton("👤تعداد افزودن عضو اجباری", callback_data="a"))
 mk.add(types.InlineKeyboardButton("➖", callback_data="down:{}".format(chat)),types.InlineKeyboardButton(str(num), callback_data="b"),types.InlineKeyboardButton("➕", callback_data="up:{}".format(chat)))
 mk.add(types.InlineKeyboardButton("⏰زمان حذف خودکار پیغام", callback_data="a"))
 mk.add(types.InlineKeyboardButton("➖", callback_data="td:{}".format(chat)),types.InlineKeyboardButton(str(time), callback_data="e"),types.InlineKeyboardButton("➕", callback_data="tu:{}".format(chat)))
 mk.add(types.InlineKeyboardButton("🗒راهنما", callback_data="helpalert"))
 return mk
# ----------------------------------------------------- #
def back_kb(chat):
 mk = types.InlineKeyboardMarkup()
 mk.add(types.InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="menu:{}".format(chat)))
 return mk
# ----------------------------------------------------- #
def get_text(chat):
 hash = "gp:{}:text".format(chat)
 text = " سلام firstname\nبرای گفتگو در گروه باید تعداد [forceadds] عضو در گروه اضافه کنی\n>تعداد عضو افزوده شده توسط شما: {useradds}"
 if redis.get(hash):
  return redis.get(hash)
 else:
  return text
# ----------------------------------------------------- #
def set_text(chat, v):
 hash = "gp:{}:text".format(chat)
 redis.set(hash, v)
# ----------------------------------------------------- #
_text_ = "BoT Running [@{}] [{}] ({})".format(bot.get_me().username, bot.get_me().first_name, bot.get_me().id)
print colored(_text_, "yellow","on_grey")
for i in admins:
 bot.send_message(i, _text_)
# ----------------------------------------------------- #
@bot.message_handler(commands=['start'])
def start(msg):
 try:
  if msg.chat.type == "private":
   text = "سلام {} \nبه ربات افزودن عضو اجباری خوش آمدید.\n🔰تیم‌رباتیڪ[ G u a r d i a n ]🔰".format(msg.from_user.first_name)
   mk = types.InlineKeyboardMarkup()
   mk.add(types.InlineKeyboardButton("🤔عملکرد ربات چگونه است؟", callback_data="abbot"))
   mk.add(types.InlineKeyboardButton("📍گروه های من", callback_data="my_gps"))
   mk.add(types.InlineKeyboardButton("📝راهنما ربات", callback_data="helpbot"))
   mk.add(types.InlineKeyboardButton("ℹ️درباره ما", callback_data="aboutus"))
   bot.reply_to(msg, text, reply_markup=mk)
   redis.sadd('membersbot',msg.from_user.id)
 except Exception as e:
  bot.reply_to(msg, "مشکلی رخ داده است، لطفا مجدد سعی کنید.")
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(content_types=['new_chat_members'])
def new_chat_members(msg):
 try:
  mems = msg.new_chat_members
  s = bot.get_chat_member(msg.chat.id, msg.from_user.id).status
  for i in mems:
   if i.id == bot.get_me().id:
    if is_admin(msg.from_user.id) or s == "creator":
     print colored("Bot Added To Group > {} | [{}] ({}) [@{}]".format(msg.chat.title, msg.from_user.first_name, msg.from_user.id, msg.from_user.username or '---'), "yellow"), colored("\n"+JalaliDatetime.now().strftime('%C'), 'cyan')
     for i in admins:
      bot.send_message(i, "گروه جدیدی در تاریخ {} به لیست گروه های تحت مدیریت ربات اضافه شد\n\nنام گروه : {}\nاطلاعات کاربر اضافه کننده :\n نام : {}\nآیدی : {}\nیوزرنیم : @{}\n".format(JalaliDatetime.now().strftime('%C'), msg.chat.title, msg.from_user.first_name, msg.from_user.id, msg.from_user.username or '---'))
     redis.sadd("{}:groups_list".format(msg.from_user.id), msg.chat.id)
     redis.set("{}:b_owner".format(msg.chat.id), msg.from_user.id)
     redis.sadd('supergroupsbot',msg.chat.id)
     bot.reply_to(msg, "{} عزیز \nگروه {} فعال گردید و به لیست گروه های شما اضافه شد.".format(msg.from_user.first_name, msg.chat.title))
    else:
     bot.reply_to(msg, "کاربر گرامی،\nبرای فعال شدن ربات باید مالک گروه/مالک ربات آن را به گروه افزوده کند.")
     bot.leave_chat(msg.chat.id)
   else:
    if msg.from_user.id != i.id:
     if i.username.endswith("bot"):
      if get_bots(msg.chat.id):
       redis.sadd("{}:adds:{}".format(msg.from_user.id, msg.chat.id), i.id)
     else:
      redis.sadd("{}:adds:{}".format(msg.from_user.id, msg.chat.id), i.id)
 except Exception as e:
  bot.reply_to(msg, "شما یک کاربر اضافه کردید")
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(regexp="[#!/][Cc][Oo][Nn][Ff][Ii][Gg]")
def config(msg):
 try:
  if msg.chat.type == "supergroup" or msg.chat.type == "group":
   s = bot.get_chat_member(msg.chat.id, msg.from_user.id).status
   if is_admin(msg.from_user.id) or s == "creator":
    for user in bot.get_chat_administrators(msg.chat.id):
     i = user.user
     set_allowed_(msg.chat.id, i.id)
   bot.reply_to(msg, "تمام ادمین های گروه در لیست مجاز قرار گرفتند\n🔰تیم‌رباتیڪ[ G u a r d i a n ]🔰")
 except Exception as e:
  bot.reply_to(msg, "مشکلی رخ داده است، لطفا مجدد سعی کنید.")
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(regexp="^[#!/][Aa][Ll][Ll][Oo][Ww][Ee][Dd] (\d+)$")
def allowed(msg):
 try:
  if msg.chat.type == "supergroup" or msg.chat.type == "group":
   s = bot.get_chat_member(msg.chat.id, msg.from_user.id).status
   if is_admin(msg.from_user.id) or s == "creator":
    user = int(re.findall("[#!/][Aa][Ll][Ll][Oo][Ww][Ee][Dd] (\d+)", msg.text)[0])
    text = set_allowed(msg.chat.id, user)
    bot.reply_to(msg, text)
 except Exception as e:
  bot.reply_to(msg, "مشکلی رخ داده است، لطفا مجدد سعی کنید.")
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(regexp="^[#!/][Nn][Oo][Tt][Aa][Ll][Ll][Oo][Ww][Ee][Dd] (\d+)$")
def notallowed(msg):
 try:
  if msg.chat.type == "supergroup" or msg.chat.type == "group":
   s = bot.get_chat_member(msg.chat.id, msg.from_user.id).status
   if is_admin(msg.from_user.id) or s == "creator":
    user = int(re.findall("^[#!/][Nn][Oo][Tt][Aa][Ll][Ll][Oo][Ww][Ee][Dd] (\d+)$", msg.text)[0])
    text = rem_allowed(msg.chat.id, user)
    bot.reply_to(msg, text)
 except Exception as e:
  bot.reply_to(msg, "مشکلی رخ داده است، لطفا مجدد سعی کنید.")
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(regexp="^[#!/][Aa][Ll][Ll][Oo][Ww][Ee][Dd]$")
def allowed(msg):
 try:
  if msg.chat.type == "supergroup" or msg.chat.type == "group":
   if msg.reply_to_message:
    s = bot.get_chat_member(msg.chat.id, msg.from_user.id).status
    if is_admin(msg.from_user.id) or s == "creator":
     user = msg.reply_to_message.from_user.id
     text = set_allowed(msg.chat.id, user)
     bot.reply_to(msg, text)
 except Exception as e:
  bot.reply_to(msg, "مشکلی رخ داده است، لطفا مجدد سعی کنید.")
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(regexp="^[#!/][Nn][Oo][Tt][Aa][Ll][Ll][Oo][Ww][Ee][Dd]$")
def notallowed(msg):
 try:
  if msg.chat.type == "supergroup" or msg.chat.type == "group":
   if msg.reply_to_message:
    s = bot.get_chat_member(msg.chat.id, msg.from_user.id).status
    if is_admin(msg.from_user.id) or s == "creator":
     user = msg.reply_to_message.from_user.id
     text = rem_allowed(msg.chat.id, user)
     bot.reply_to(msg, text)
 except Exception as e:
  bot.reply_to(msg, "مشکلی رخ داده است، لطفا مجدد سعی کنید.")
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(regexp="^[#!/][Ll][Ee][Aa][Vv][Ee]$")
def leave(msg):
 try:
  if msg.chat.type == "supergroup" or msg.chat.type == "group":
   if is_admin(msg.from_user.id):
    bot.leave_chat(msg.chat.id)
 except Exception as e:
  bot.reply_to(msg, "مشکلی رخ داده است، لطفا مجدد سعی کنید.")
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(regexp="^[#!/][Pp][Aa][Nn][Ee][Ll]$")
def panel(msg):
 try:
  if msg.chat.type == "supergroup" or msg.chat.type == "group":
   s = bot.get_chat_member(msg.chat.id, msg.from_user.id).status
   if is_admin(msg.from_user.id) or s == "creator":
    bot.reply_to(msg, "تنظیمات گروه {}".format(msg.chat.title), reply_markup=main_gp(msg.chat.id))
 except Exception as e:
  bot.reply_to(msg, "مشکلی رخ داده است، لطفا مجدد سعی کنید.")
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(regexp="^[!#/][Ss][Ee][Tt][Tt][Ee][Xx][Tt] (.*)")
def set(msg):
 try:
  if msg.chat.type == "supergroup" or msg.chat.type == "group":
   s = bot.get_chat_member(msg.chat.id, msg.from_user.id).status
   if is_admin(msg.from_user.id) or s == "creator":
    text = msg.text.replace("{}".format(msg.text.split()[0]), '')
    set_text(msg.chat.id, text)
    bot.reply_to(msg, "متن جدید ذخیره شد\n\n"+text)
 except Exception as e:
  bot.reply_to(msg, "مشکلی رخ داده است، لطفا مجدد سعی کنید.")
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.callback_query_handler(func=lambda q: True)
def callback_inline(q):
 try:
  s = q.data.split(":")
  v = s[0]
  cmds = ['menu', 'alloweds_list', 'up', 'down', 'status', 'bots', 'tu', 'td']
  if v in cmds:
   chat = int(s[1])
   status = bot.get_chat_member(chat, q.from_user.id).status
   if is_admin(q.from_user.id) or status == "creator":

    if v == "menu":
     bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text="تنظیمات گروه "+ get_title(chat), reply_markup=main_gp(chat))

    if v == "alloweds_list":
     hash = redis.smembers("{}:alloweds".format(chat))
     text = "👥 لیست افراد مجاز گروه:\n"
     i = 0
     for k in hash:
      i += 1
      text += "`{}` - *{}*\n".format(i, k)
     if len(hash) <= 0:
      text = "`لیست افراد مجاز گروه خالی میباشد.`"
     bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text=text, reply_markup=back_kb(chat), parse_mode="MarkDown")

    if v == "up":
     num = get_num(chat) + 1
     set_num(chat, num)
     bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text="تنظیمات گروه "+get_title(chat), reply_markup=main_gp(chat))

    if v == "down":
     num = get_num(chat) - 1
     if num != 0:
      set_num(chat, num)
      bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text="تنظیمات گروه "+get_title(chat), reply_markup=main_gp(chat))
     else:
      bot.answer_callback_query(q.id, "حداقل عدد انتخابی برای این قابلیت {1} میباشد.")

    if v == "status":
     set_status(chat)
     bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text="تنظیمات گروه "+get_title(chat), reply_markup=main_gp(chat))

    if v == "bots":
     set_bots(chat)
     bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text="تنظیمات گروه "+get_title(chat), reply_markup=main_gp(chat))

    if v == "tu":
     num = get_time(chat) + 1
     set_time(chat, num)
     bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text="تنظیمات گروه "+get_title(chat), reply_markup=main_gp(chat))

    if v == "td":
     num = get_time(chat) - 1
     if num >= 3:
      set_time(chat, num)
      bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text="تنظیمات گروه "+get_title(chat), reply_markup=main_gp(chat))
     else:
      bot.answer_callback_query(q.id, "حداقل عدد انتخابی برای این قابلیت {3} میباشد.")

   else:
    bot.answer_callback_query(q.id, "شما مالک گروه/مالک ربات نیستید و امکان تغییر تنظیمات را ندارید.")
  else:
   if q.data == "my_gps":
    hash = redis.smembers("{}:groups_list".format(q.from_user.id))
    mk = types.InlineKeyboardMarkup()
    text = "لیست گروه های شما:"
    for gp in hash:
     mk.add(types.InlineKeyboardButton(get_title(gp), callback_data="gpn_{}".format(gp)))
    if len(hash) <= 0:
     text = "شما گروهی در ربات ندارید"
    mk.add(types.InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="smenu"))
    bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text='`'+text+'`', reply_markup=mk, parse_mode="MarkDown")

   if q.data == "helpbot":
    mk = types.InlineKeyboardMarkup()
    text = """
به بخش راهنما کار با ربات خوش امدید:

1. [!/#]panel -- دریافت تنظیمات گروه

2. [!/#]settext text -- تنظیم متن هشدار افزودن عضو برای کاربر
همچنین شما میتوانید از یکی از مقدایر زیر :

● firstname - نمایش نام کاربر
● lastname - نمایش نام خانوادگی کاربر
● username - نمایش یوزرنیم کاربر
● forceadds - نمایش تعداد اضافه کردن اجباری گروه
● useradds - نمایش تعداد کاربرانی که کاربر اضافه کرده است
● groupname - نام گروه

در متن خود استفاده کنید

3. [!/#]allowed id | reply -- اضافه کردن کاربر به لیست مجاز با دو عملکرد شناسه کاربر | ریپلی

4. [!/#]notallowed id | reply -- حذف کردن کاربر از لیست مجاز با دو عملکرد شناسه کاربر | ریپلی

5. [!/#]config -- افزودن تمامی ادمین های گروه به لیست مجاز کاربران

6. [!/#]leave -- خروج ربات از گروه

"""
    hash = redis.smembers("{}:groups_list".format(q.from_user.id))
    if len(hash) <= 0:
     bot.answer_callback_query(callback_query_id=q.id, show_alert=True, text="متن راهنما فقط برای کاربرانی که ربات را در گروه افزوده و فعال کرده اند نمایش داده میشود")
    else:
     mk.add(types.InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="smenu"))
     bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text=text, reply_markup=mk, parse_mode="HTML")

   if q.data == "abbot":
    mk = types.InlineKeyboardMarkup()
    text = """
نحوه کارکرد ربات به چه شکل میباشد؟

● نحوه کار ربات به این شکل است که افرادی بجز مالک ربات و مالک گروه برای گفتگو در گروه نیازمند افزودن عضو به تعداد مشخص شده توسط شما در گروه میباشند.
● لازم به ذکر است شما علاوه بر این که میتوانید تعداد افزودن عضو برای گفتگو در گروه را تایین کنید میتوانید پارامتر های زیر را هم به دلخواه تنظیم کنید.
1- تنظیم دسترسی افزودن ربات بجای عضو جهت حذف محدودیت گفتگو در گروه،
2- تنظیم پیغام حذف خودکار پیغام هشدار افزودن عضو بعد از ارسال در گروه،
3- فعال کردن یا غیرفعال کردن ربات در گروه،
و قابلیت های دیگر که ان ها رو در متن راهنما برای شما معرفی کردیم.
🔰تیم‌رباتیڪ[ G u a r d i a n ]🔰
"""
    mk.add(types.InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="smenu"))
    bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text=text, reply_markup=mk, parse_mode="HTML")

   if q.data == "smenu":
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🤔عملکرد ربات چگونه است؟", callback_data="abbot"))
    mk.add(types.InlineKeyboardButton("📍گروه های من", callback_data="my_gps"))
    mk.add(types.InlineKeyboardButton("📝راهنما ربات", callback_data="helpbot"))
    mk.add(types.InlineKeyboardButton("ℹ️درباره ما", callback_data="aboutus"))
    bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text='`بازگشت به منوی اصلی`', reply_markup=mk, parse_mode="MarkDown")
   if q.data.startswith("gpn"):
    gp = int(q.data.replace("gpn_",""))
    kb = main_gp(gp)
    kb.add(types.InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="my_gps"))
    bot.edit_message_text(chat_id=q.message.chat.id, message_id=q.message.message_id, text='`تنظیمات گروه` '+get_title(gp), reply_markup=kb, parse_mode="MarkDown")

   if q.data == "aboutus":
    bot.answer_callback_query(callback_query_id=q.id, show_alert=True, text="طراحی شده توسط تیم رباتیک گاردین\n\nhttps://t.me/CLI_guardian_TG")
	
   if q.data == "helpalert":
    bot.answer_callback_query(callback_query_id=q.id, show_alert=True, text="برای مشاهده 📝راهنما ربات در خصوصی ربات عبارت\n /start\nرا ارسال کنید.")
 except ApiException:
  pass
 except Exception as e:
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(regexp="^[#!/][Bb][Cc] (.*)")
def broadcastusers(msg):
    if is_admin(msg.from_user.id):
        text = msg.text.replace("/bc ","")
        member = redis.smembers('membersbot')
        for id in member:
            try:
                bot.send_message(id, "{}".format(text), parse_mode="Markdown")
            except:
                redis.srem('membersbot', id)
# ----------------------------------------------------- #
@bot.message_handler(regexp="^[#!/][Ss][Tt][Aa][Tt][Ss]$")
def stats(msg):
    if is_admin(msg.from_user.id):
        user = str(redis.scard('membersbot'))
        supergroups = str(redis.scard('supergroupsbot'))
        text = '*تعداد کاربران ربات : {}*\n*تعداد سوپرگروه های ربات : {}*'.format(user, supergroups)
        bot.reply_to(msg, text,parse_mode='Markdown')
# ----------------------------------------------------- #
@bot.message_handler(content_types=['text','audio','document','game','photo','sticker','video','voice','video_note','contact','location','venue'])
def check(msg):
 try:
  s = bot.get_chat_member(msg.chat.id, msg.from_user.id).status
  if not is_admin(msg.from_user.id) and not s == "creator" and not is_allowed(msg.chat.id, msg.from_user.id) and msg.chat.type != "private":
   num = get_num(msg.chat.id)
   u = redis.scard("{}:adds:{}".format(msg.from_user.id, msg.chat.id))
   if u < num and get_status(msg.chat.id):
    bot.delete_message(msg.chat.id, msg.message_id)
    text = get_text(msg.chat.id).replace("firstname",msg.from_user.first_name).replace("lastname",msg.from_user.last_name or "---").replace("username",msg.from_user.username or "---").replace("forceadds",str(num)).replace("useradds",str(u)).replace("groupname",msg.chat.title)
    m = bot.send_message(msg.chat.id, text)
    th = Timer(get_time(msg.chat.id), bot.delete_message, args=(msg.chat.id, m.message_id))
    th.start()
 except Exception as e:
  print colored(e, "red")
# ----------------------------------------------------- #
@bot.message_handler(content_types=['left_chat_member'])
def left(msg):
 if msg.left_chat_member.id == bot.get_me().id:
  o = redis.get("{}:b_owner".format(msg.chat.id))
  redis.srem("{}:groups_list".format(o), msg.chat.id)
bot.polling(True)
