from telebot.types import *
from config import *



def start_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("👤Профиль", callback_data='profile'), InlineKeyboardButton("🛒Категории", callback_data="catalogs"))
    keyboard.row(InlineKeyboardButton("⚙️Тех. Поддержка", f"https://t.me/{SUPPORT_USERNAME}"), InlineKeyboardButton("📚Новостной канал", CHANNEL_LINK))
    keyboard.row(InlineKeyboardButton("💸Пополнить баланс", callback_data="balance"))
    return keyboard

def unsub_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Подписаться", CHANNEL_LINK))
    keyboard.row(InlineKeyboardButton("Я подписался", callback_data="start"))
    return keyboard

def profile_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("🤝Реферальная система", callback_data="ref_system"), InlineKeyboardButton("💸Пополнить баланс", callback_data="balance"))
    keyboard.row(InlineKeyboardButton("⬅️Вернуться", callback_data="start"))
    return keyboard

def balance_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("💎Crypto Bot", callback_data="cryptopay"), InlineKeyboardButton("💠Crystal Pay", callback_data="crystalpay"))
    keyboard.row(InlineKeyboardButton("⬅️Вернуться", callback_data="profile"))
    return keyboard


def ref_system_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("⬅️Вернуться", callback_data="start"))
    return keyboard


def catalog_kb(products):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("✈️ Telegram accounts", callback_data="submit_fiz_rf"))
    keyboard.row(InlineKeyboardButton("🎁 Telegram premium", callback_data="buy_premium"), InlineKeyboardButton("⭐️ Telegram Stars", callback_data="buy_stars"))
    # catalogs = set()
    # for product in products:
    #     catalogs.add(product[4])
    # for catalog in catalogs:
    #     keyboard.row(InlineKeyboardButton(catalog, callback_data=catalog))
    keyboard.row(InlineKeyboardButton("⬅️Вернуться", callback_data="start"))
    return keyboard


def submit_fiz_rf_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("✅Купить", callback_data="buy_fiz_rf"), InlineKeyboardButton("⛔️Отмена", callback_data="catalogs"))
    return keyboard


def user_agreement_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("🔍 Соглашениe", USER_AGREEMENT_LINK), InlineKeyboardButton("✈️ Я ознакомился", callback_data="user_agree"))
    return keyboard

def submit_buy(product):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("💸 Приобрести", callback_data=f"buy_{product}"), InlineKeyboardButton("❌ Отмена", callback_data="catalogs"))
    return keyboard


def buyed_shit_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("⚜️Администратор", f"tg://user?id={OWNER_ID}"))
    keyboard.row(InlineKeyboardButton("🔰Главное меню", callback_data="start"))
    return keyboard