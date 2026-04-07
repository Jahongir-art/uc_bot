

import telebot
from telebot.types import ReplyKeyboardMarkup

TOKEN = "8533207489:AAFbpwG72z1GQxpBM3uzkOJhXhAxLE87_z8"
ADMIN_ID = 8248560591
CARD = "Humo 4073 4200 4928 8487  Ulashov Jahongir"

bot = telebot.TeleBot(TOKEN)

user_data = {}

prices = {
    30: "6 500",
    60: "12 500",
    120: "25 000",
    180: "37 000",
    325: "58 000",
    385: "72 000",
    660: "115 000",
    720: "126 000",
    985: "173 000",
    1320: "230 000",
    1800: "283 000",
    2125: "355 000",
    2460: "405 000",
    3850: "570 000",
    4510: "680 000",
    5650: "850 000",
    8100: "1 110 000",
    11950: "1 700 000",
    24300: "3 500 000"
}

# 🔹 MENU
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 UC sotib olish", "📊 Narxlar")
    return markup

# 🔹 ORQAGA BUTTON
def back_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⬅️ Orqaga")
    return markup

# START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Xush kelibsiz!", reply_markup=main_menu())

# ORQAGA
@bot.message_handler(func=lambda m: m.text == "⬅️ Orqaga")
def back(message):
    bot.send_message(message.chat.id, "🔙 Bosh menu", reply_markup=main_menu())

# UC TANLASH
@bot.message_handler(func=lambda m: m.text == "💰 UC sotib olish")
def buy_uc(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("30 UC", "60 UC", "120 UC")
    markup.add("180 UC", "325 UC", "385 UC")
    markup.add("660 UC", "720 UC", "985 UC")
    markup.add("1320 UC", "1800 UC", "2125 UC")
    markup.add("2460 UC", "3850 UC", "4510 UC")
    markup.add("5650 UC", "8100 UC", "11950 UC", "24300 UC")
    markup.add("⬅️ Orqaga")

    msg = bot.send_message(message.chat.id, "UC tanlang 👇", reply_markup=markup)
    bot.register_next_step_handler(msg, get_uc)

# UC OLISH
def get_uc(message):
    if message.text == "⬅️ Orqaga":
        return back(message)

    try:
        uc = int(''.join(filter(str.isdigit, message.text)))

        if uc not in prices:
            raise Exception

        user_data[message.chat.id] = {"uc": uc}
        price = prices[uc]

        bot.send_message(message.chat.id,
                         f"💰 Narxi: {price} so'm\n\n💳 Karta:\n{CARD}",
                         reply_markup=back_menu())

        msg = bot.send_message(message.chat.id, "🎮 PUBG ID yuboring:")
        bot.register_next_step_handler(msg, get_id)

    except:
        msg = bot.send_message(message.chat.id, "❌ Tugmadan tanlang!")
        bot.register_next_step_handler(msg, get_uc)

# PUBG ID
def get_id(message):
    if message.text == "⬅️ Orqaga":
        return back(message)

    user_data[message.chat.id]["pubg_id"] = message.text

    msg = bot.send_message(message.chat.id, "📸 Chekni rasm qilib yuboring:", reply_markup=back_menu())
    bot.register_next_step_handler(msg, get_check)

# CHEK
def get_check(message):
    if message.text == "⬅️ Orqaga":
        return back(message)

    if message.content_type == 'photo':
        data = user_data[message.chat.id]

        bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!", reply_markup=main_menu())

        bot.send_photo(ADMIN_ID, message.photo[-1].file_id,
                       caption=f"🛒 Yangi buyurtma!\n\n"
                               f"👤 Ism: {message.from_user.first_name}\n"
                               f"🆔 TG ID: {message.from_user.id}\n"
                               f"🎮 PUBG ID: {data['pubg_id']}\n"
                               f"💰 UC: {data['uc']}")

    else:
        msg = bot.send_message(message.chat.id, "❌ Rasm yuboring!")
        bot.register_next_step_handler(msg, get_check)

# NARXLAR
@bot.message_handler(func=lambda m: m.text == "📊 Narxlar")
def show_prices(message):
    text = "📊 UC Narxlari:\n\n"
    for uc, price in prices.items():
        text += f"{uc} UC — {price} so'm\n"

    bot.send_message(message.chat.id, text, reply_markup=back_menu())

bot.polling()