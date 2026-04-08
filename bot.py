
import telebot
from telebot import types

# ============================
# BOT VA ADMIN CONFIG
# ============================
TOKEN = "8533207489:AAFbpwG72z1GQxpBM3uzkOJhXhAxLE87_z8"  # Bot token
ADMIN_ID = 8248560591  # Admin TG ID

bot = telebot.TeleBot(TOKEN)

# ============================
# UC NARXLARI
# ============================
prices = {
    "30": "6.500",
    "60": "12.500",
    "120": "25.000",
    "180": "37.000",
    "325": "58.000",
    "385": "72.000",
    "660": "116.000",
    "720": "127.000",
    "985": "173.000",
    "1320": "230.000",
    "1800": "283.000",
    "2125": "355.000",
    "2460": "405.000",
    "3850": "570.000",
    "4510": "680.000",
    "5650": "850.000",
    "8100": "1.110.000",
    "11950": "1.700.000",
    "24300": "3.500.000"
}

# ============================
# BUYURTMALAR TEMP STORAGE
# ============================
pending_orders = {}

# ============================
# /start KOMANDASI
# ============================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! UC sotib olish uchun /buy komandasini yuboring.")


# ============================
# BUY UC
# ============================
@bot.message_handler(commands=['buy'])
def buy_uc(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for uc_amount in prices.keys():
        markup.add(uc_amount)
    msg = bot.send_message(user_id, "UC miqdorini tanlang 👇", reply_markup=markup)
    bot.register_next_step_handler(msg, get_uc_amount)


def get_uc_amount(message):
    user_id = message.from_user.id
    uc = message.text
    if uc not in prices:
        msg = bot.send_message(user_id, "❌ Noto'g'ri miqdor, qayta tanlang:")
        bot.register_next_step_handler(msg, get_uc_amount)
        return

    pending_orders[user_id] = {'uc': uc, 'username': message.from_user.username}
    msg = bot.send_message(user_id, f"UC: {uc}\nNarxi: {prices[uc]} so'm\nPul miqdorini yuboring:")
    bot.register_next_step_handler(msg, get_paid_amount)


def get_paid_amount(message):
    user_id = message.from_user.id
    try:
        amount = int(message.text.replace(".", "").replace(",", ""))
    except ValueError:
        msg = bot.send_message(user_id, "❌ Pul summasini raqam bilan yuboring:")
        bot.register_next_step_handler(msg, get_paid_amount)
        return

    pending_orders[user_id]['paid_amount'] = amount
    msg = bot.send_message(user_id, "✅ Endi chek rasmini yuboring:")
    bot.register_next_step_handler(msg, get_check)


# ============================
# CHECK QABUL QILISH VA TASDIQLASH
# ============================
def get_check(message):
    user_id = message.from_user.id
    data = pending_orders.get(user_id, {})

    if not message.photo:
        msg = bot.send_message(user_id, "❌ Iltimos, chek rasmini yuboring.")
        bot.register_next_step_handler(msg, get_check)
        return

    check_file_id = message.photo[-1].file_id
    data['check_file_id'] = check_file_id
    pending_orders[user_id] = data

    # Avto tasdiqlash
    if auto_verify_check(data):
        confirm_order(user_id)
    else:
        bot.send_message(user_id, "❌ Chek tasdiqlanmadi, iltimos qayta yuboring.")
        msg = bot.send_message(user_id, "Check yuboring:")
        bot.register_next_step_handler(msg, get_check)


def auto_verify_check(data):
    """Simple avto tekshiruvchi, hozirgi narx va to‘lovni solishtiradi"""
    uc = data.get('uc')
    price = int(prices[uc].replace(".", "").replace(",", ""))
    paid_amount = data.get('paid_amount', 0)
    return paid_amount >= price


def confirm_order(user_id):
    data = pending_orders.get(user_id)
    username = f"@{data.get('username')}" if data.get('username') else "Noma'lum"
    uc = data['uc']
    price = prices[uc]

    caption = f"""✅ Yangi buyurtma tasdiqlandi!

👤 Username: {username}
🆔 TG ID: {user_id}
🎮 UC: {uc}
💵 Narx: {price} so'm
"""
    # Adminga yuborish
    bot.send_photo(ADMIN_ID, data['check_file_id'], caption=caption)
    # Userga ham yuborish
    bot.send_message(user_id, "✅ Sizning buyurtmangiz tasdiqlandi! Adminga yuborildi.")
    # Buyurtmani saqlashdan o'chirish
    pending_orders.pop(user_id, None)


# ============================
# BOT POLLING
# ============================
bot.polling(non_stop=True)