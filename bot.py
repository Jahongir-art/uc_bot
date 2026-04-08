import telebot
from telebot import types

TOKEN = "TOKENINGNI_QOY"
ADMIN_ID = 8248560591
CHANNEL = "@ulashov_uc"

# 💳 KARTA
CARD = "4073 4200 4928 8487"
CARD_NAME = "Ulashov Jahongir"

bot = telebot.TeleBot(TOKEN)

user_data = {}

prices = {
    "30": "6 500",
    "60": "12 500",
    "120": "25 000",
    "180": "37 000",
    "325": "58 000",
    "385": "72 000",
    "660": "116 000",
    "720": "127 000",
    "985": "173 000",
    "1320": "230 000",
    "1800": "283 000",
    "2125": "355 000",
    "2460": "405 000",
    "3850": "570 000",
    "4510": "680 000",
    "5650": "850 000",
    "8100": "1 110 000",
    "11950": "1 700 000",
    "24300": "3 500 000"
}

# MENU
def menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 UC Narxlari", "🛒 UC Xarid")
    markup.add("📢 Kanal", "👨‍💼 Admin")
    return markup

def footer():
    return "\n\n📢 Kanal: https://t.me/ulashov_uc"

# START
@bot.message_handler(commands=['start'])
def start(message):
    try:
        member = bot.get_chat_member(CHANNEL, message.from_user.id)
        if member.status in ['left', 'kicked']:
            bot.send_message(message.chat.id, "❌ Avval kanalga obuna bo‘ling!\nhttps://t.me/ulashov_uc")
            return
    except:
        pass

    bot.send_message(message.chat.id, "👋 Xush kelibsiz!", reply_markup=menu())

# NARXLAR
@bot.message_handler(func=lambda m: m.text == "💰 UC Narxlari")
def show_prices(message):
    text = "💰 UC Narxlari:\n\n"
    for uc, price in prices.items():
        text += f"{uc} UC — {price} so'm\n"

    bot.send_message(message.chat.id, text + footer())

# UC XARID
@bot.message_handler(func=lambda m: m.text == "🛒 UC Xarid")
def buy_uc(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for uc in prices.keys():
        markup.add(f"{uc} UC")

    markup.add("🔙 Orqaga")

    msg = bot.send_message(message.chat.id, "UC tanlang 👇", reply_markup=markup)
    bot.register_next_step_handler(msg, get_uc)

def get_uc(message):
    if message.text == "🔙 Orqaga":
        start(message)
        return

    uc = ''.join(filter(str.isdigit, message.text))

    if uc not in prices:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri tanlov")
        return

    user_data[message.chat.id] = {"uc": uc}

    # 💳 KARTA + SUMMA CHIQADI
    bot.send_message(
        message.chat.id,
        f"""💳 To‘lov qilish:

💰 UC: {uc}
💵 Narx: {prices[uc]} so'm

💳 Karta: {CARD}
👤 Ism: {CARD_NAME}

📸 To‘lovdan so‘ng chek yuboring!"""
    )

    bot.register_next_step_handler(message, get_check)

# CHEK
def get_check(message):
    if message.content_type != 'photo':
        bot.send_message(message.chat.id, "❌ Iltimos chek rasmini yuboring")
        return

    data = user_data.get(message.chat.id)

    username = message.from_user.username
    if username:
        username = "@" + username
    else:
        username = "Username yo‘q"

    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!")

    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"""🛒 Yangi buyurtma!

👤 Username: {username}
🆔 TG ID: {message.from_user.id}
💰 UC: {data['uc']}
💵 Narx: {prices[data['uc']]} so'm
"""
    )

# RUN
bot.infinity_polling()