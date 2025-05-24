from telebot import TeleBot
from telebot.types import *
from config import *
from sqlite3 import Connection
from time import time, ctime
from kb import *
from CryptoPay import CryptoPay
from CrystalPay import CrystalPay
from os import listdir, system
from threading import Thread
from pyrogram import Client
import requests
import json




CryptoPay = CryptoPay(CRYPTOBOT_TOKEN)
CrystalPay = CrystalPay(CRYSTALPAY_AUTH_LOGIN, CRYSTALPAY_AUTH_SECRET)
bot = TeleBot(BOT_TOKEN, "HTML")
con = Connection("db.db", isolation_level=None, check_same_thread=False)
api_key = "db14f2bb-aa03-4d45-8269-3a0254ab0fb1"
def get_data(id: int):
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        data = cursor.fetchone()
        if data is None:
            data = (id, 0.0, 0.0, time(), None, False)
            cursor.execute("INSERT INTO users VALUES(?,?,?,?,?,?)", data)
        return data
def get_products():
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        res = []
        for product in products:
            res.append(product[0])
        return res
def get_categories():
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    catalogs = set()
    for product in products:
        catalogs.add(product[4])
    return list(catalogs)
def CqueryFunc(*args):
    return lambda sth: sth.data in args    
def is_sub(message: Message):
    print("is_sub funcrion")
    try:
        if bot.get_chat_member(CHANNEL_ID, message.from_user.id).status == "left":
            return True
        else:
            False
    except:
        return False



@bot.message_handler(func=is_sub)
def not_sub(message):
    bot.send_message(message.chat.id, f"<b>⚠️ Для использования бота необходимо подписаться на канал:</b>", reply_markup=unsub_kb())



@bot.callback_query_handler(lambda call: call.data == "submit_fiz_rf")
def submit_fiz_rf_handler(call):
    data = get_data(call.from_user.id)
    if data[1] <= 2.5:
        bot.answer_callback_query(call.id, "На вашем балансе недостаточно средств")
    else:
        bot.edit_message_text(f"""<b>🚀 Товар: ✈️ Telegram accounts | 2.5$     
🎁 Описание: <u>Полностью новый телеграм аккаунт для вас в любое время суток 🌐</u></b>""", call.message.chat.id, call.message.id, reply_markup=submit_fiz_rf_kb())


@bot.message_handler(['online'])
def online_hander(message: Message):
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT  * FROM users")
        bot.reply_to(message, f"<b>В боте {len(cursor.fetchall())} пользователей</b>")


@bot.message_handler(['db'])
def database(message):
    if message.from_user.id != CODER_ID: return
    bot.send_document(message.chat.id, open("db.db", 'rb').read())


@bot.callback_query_handler(lambda call: call.data == "ref_system")
def ref_system_handler(call: CallbackQuery):
    data = get_data(call.from_user.id)
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE ref=?", (call.from_user.id,))
        refs = cursor.fetchall()
    bot.edit_message_text(f"""<b>🔗 Ваша ссылка: ссылка которую можна скопировать при нажатии
💵 Заработано: {data[2]}$
🌐 Количество рефералов: {len(refs)}

🚀 Вы будете получать: 5% от всех пополнений рефералов</b>""", call.message.chat.id, call.message.id, reply_markup=ref_system_kb())



@bot.callback_query_handler(CqueryFunc("user_agree"))
def user_agree_handler(call: CallbackQuery):
    with con:
        con.cursor().execute("UPDATE users SET license_submit=? WHERE id=?", (True, call.from_user.id))
    bot.answer_callback_query(call.id, "Спасибо! приятного использования бота!")
    start_handler(call)


def code_hadn(message: Message, phone_number: str):
    app = sessions_adding[phone_number][0]
    try:
        code = message.text.strip()
        sCode = sessions_adding[phone_number][1]
        app.sign_in(phone_number, sCode.phone_code_hash, code)
        app.disconnect()
        bot.reply_to(message, "сессия успешно создана")
    except:
        try:
            app.disconnect()
        except:
            ...
        os.remove(f"sessions/{phone_number}.session")
        bot.reply_to(message, "Ошибка, пробуй заново")

import asyncio

def phone_adding_handlea(message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    phone = message.text.strip().replace(" ", "")
    app = Client(f"sessions/{phone}", 25389095, "a715da4e82e7a2bab63fef6364c62596")
    app.connect()
    sCode = app.send_code(phone)
    sessions_adding[phone] = [app, sCode]
    msg = bot.send_message(message.chat.id, "Код отправлен, скинь его")
    bot.register_next_step_handler(msg, code_hadn, phone)
    


sessions_adding = {"79998887766": ["ClientObject", "sentCodeObject"]}
@bot.message_handler(['add_session'])
def add_session_handler(message: Message):
    if message.from_user.id != OWNER_ID: return
    msg = bot.reply_to(message, "Отправь номер телефона")
    bot.register_next_step_handler(msg, phone_adding_handlea)


@bot.callback_query_handler(CqueryFunc(*get_products()))
def fiz_rf_handle(call: CallbackQuery):
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM products WHERE shortname=?", (call.data,))
        product_info = cursor.fetchone()
        bot.edit_message_text(f"<b>🚀 Товар: {product_info[1]} | {product_info[5]}$\n🎁 Описание: {product_info[2]}</b>", call.message.chat.id, call.message.id, reply_markup=submit_buy(call.data))


@bot.callback_query_handler(lambda call: call.data == "fiz_rf_code")
def fiz_rf_code_handle(call: CallbackQuery):
    session_name = call.message.text.split("\n")[5].replace('📱 Номер телефона: ', "")
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM codes WHERE session_name=?", (session_name,))
        session_data = cursor.fetchone()
        if session_data is None:
            bot.answer_callback_query(call.id, "Покупка не найдена!", True)
            catalogs_handler(call)
        elif session_data[2] is None:
            bot.answer_callback_query(call.id, "Код еще не пришел, подождите еще немного!")
        else:
            cursor.execute("UPDATE users SET balance=balance-? WHERE id=?", (2.5, call.from_user.id))
            bot.send_message(OWNER_ID, f"Пользователь {call.from_user.id} купил сессию с номером {session_data[0]} за 2.5$")
            bot.edit_message_text(f"<b>Номер телефона: <code>{session_name}</code>\n\nКод: <tg-spoiler>{session_data[2]}</tg-spoiler></b>", call.message.chat.id, call.message.id)


@bot.callback_query_handler(lambda call: call.data.startswith("premium;"))
def submit_premium(call: CallbackQuery):
    data = get_data(call.from_user.id)
    month = call.data.split(";")[1]
    username = call.data.split(";")[2]
    url2 = "https://tg.parssms.info/v1/premium/price"
    payload2 = ""
    headers2 = {
        'Content-Type': 'application/json',
        'api-key': api_key,
        }
    response2 = requests.request("GET", url2, headers=headers2, data=payload2).json()
    for priceinfo in response2:
        match priceinfo['duration']:
            case "1 year":
                duration = 12
            case "6 months":
                duration = 6
            case "3 months":
                duration = 3
        if duration == int(month):
            price = priceinfo['approx_price_usd'].replace("$", "")
    if data[1] < float(price) * TG_SERVICE_EXTRA:
        bot.answer_callback_query(call.id, "На вашем балансе недостаточно средств!")
    else:
        with con:
            cursor = con.cursor()
            cursor.execute("UPDATE users SET balance=balance-? WHERE id=?", (float(price), call.from_user.id))
            url = "https://tg.parssms.info/v1/premium/payment"
            payload = json.dumps({
            "query": username,
            "months": str(month)
            })
            headers = {
            'Content-Type': 'application/json',
            'api-key': api_key
            }
            response = requests.post(url, headers=headers, data=payload).json()
            if "message" in response:
                if "not enough" in response['message']:
                    bot.send_message(OWNER_ID, f"Нужно пополнить кошелек, {response['message']}")
                    bot.answer_callback_query(call.id, "На данный момент невозможно приобрести телеграм премиум, обратитесь к администратору", True)
                else:
                    cursor.execute("UPDATE users SET balance=balance-? WHERE id=?", (float(price) * TG_SERVICE_EXTRA, call.from_user.id))
                    bot.edit_message_text(f"<b>Успешное пополнение!\n\nКомментарий: {response['message']}\nID транзакции: {response['transaction_id']}</b>", call.message.chat.id, call.message.id, reply_markup=start_kb())
                    bot.send_message(OWNER_ID, f"Пользователь {call.from_user.username} купил телеграм премиум на {month} месяцев за ${float(price) * TG_SERVICE_EXTRA} для {username}")



def premiumuserInfo(message, old_id):
    data = get_data(message.from_user.id)
    username = message.text.strip()
    url = "https://tg.parssms.info/v1/premium/search"
    payload = json.dumps({
 "query": username,
 "months": "3"
})
    headers = {
 'Content-Type': 'application/json',
 'api-key': api_key
}
    response = requests.post(url, headers=headers, data=payload).json()
    if not response['ok']:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("Отмена", callback_data="premiumCancel"))
        msg = bot.edit_message_text(f"""<b>💎 Telegram Premium          
                             
• 🎁 3/6/12 месяцев – автоматическая отправка подарком.                                        

• Отправьте @username получателя, которому хотите подарить премиум (премиум поступит автоматически, в течение 20 секунд)\n\nТакого пользователя не существует</b>""", message.chat.id, old_id, reply_markup=keyboard)
        bot.register_next_step_handler(msg, premiumuserInfo, msg.id)
    else:
        url2 = "https://tg.parssms.info/v1/premium/price"
        payload2 = ""
        headers2 = {
        'Content-Type': 'application/json',
        'api-key': api_key,
        }
        response2 = requests.request("GET", url2, headers=headers2, data=payload2).json()
        keyboard = InlineKeyboardMarkup()
        for priceinfo in response2:
            match priceinfo['duration']:
                case "1 year":
                    pricename = "1 год"
                    duration = 12
                case "6 months":
                    pricename = "6 месяцев"
                    duration = 6
                case "3 months":
                    duration = 3
                    pricename = "3 месяца"
            keyboard.row(InlineKeyboardButton(f"🔰 {pricename} | {round(float(priceinfo['approx_price_usd'].replace('$', '')) * TG_SERVICE_EXTRA, 2)}", callback_data=f"premium;{duration};{username}"))
        keyboard.row(InlineKeyboardButton("⬅️Отмена", callback_data="tgCancel"))
        bot.edit_message_text(f"""<b>🛒 Покупка 🎁 Telegram Premium

🏦 Баланс: <code>{data[1]}$</code>

👤 Получатель: <a href="https://t.me/{username}">{response['found']['name']}</a>

Выберите срок подписки которую хотите подарить</b>""", message.chat.id, old_id, reply_markup=keyboard)
    try:
        bot.delete_message(message.chat.id, message.id)
    except:
        ...


@bot.callback_query_handler(lambda call: call.data.startswith("strs"))
def buying_stars_handler(call: CallbackQuery):
    username = call.data.split(";")[1]
    count = int(call.data.split(';')[2])
    amount = count * 0.015 * TG_SERVICE_EXTRA
    data = get_data(call.from_user.id)
    if data[1] < amount:
        bot.answer_callback_query(call.id, f"На вашем балансе недостаточно средств!\n\nПополните его на ${round(amount - data[1], 2)} и попробуйте снова!", True)
        return 
    url = "https://tg.parssms.info/v1/stars/payment"
    payload = json.dumps({
 "query": username,
 "quantity": str(count)
})
    headers = {
 'Content-Type': 'application/json',
 'api-key': api_key
}
    response = requests.post(url, headers=headers, data=payload).json()
    if "error" in response['message']:
        need = response['message'].split("Ton, Needs: ")[1].split(" Ton")[0]
        bot.send_message(OWNER_ID, f"Нужно пополнить TON кошелек на {need} TON")
        bot.answer_callback_query(call.id, "Неизвестная ошибка!\nОбратитесь к администратору чтобы решить проблему!")
    else:
        with con: 
            cursor = con.cursor()
            cursor.execute("UPDATE users SET balance=balance-? WHERE id=?", (amount, call.from_user.id))
        bot.send_message(OWNER_ID, f"{call.from_user.username} купил {count} звезд для {username} за {amount}")
        bot.edit_message_text(f"<b>Успешное пополнение!\n\nКомментарий: {response['message']}\nID транзакции: {response['transaction_id']}</b>", call.message.chat.id, call.message.id, reply_markup=start_kb())




def starscounthandler(message, old_id, username, name):
    data = get_data(message.from_user.id)
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("⬅️Отмена", callback_data="tgCancel"))
    try:
        count = int(message.text.strip())
        if count < 50 or count > 1000000:
            msg = bot.edit_message_text(f"""💫 Укажите количество звёзд для {name}:

Минимум: 50 звезд
Максимум: 1 000 000 звезд
                                        
Вы можете купить от 50 до 1млн звезд</b>""", message.chat.id, old_id, reply_markup=keyboard)
            bot.register_next_step_handler(msg, starscounthandler, msg.id, username, name)
        else:
            keyboard = InlineKeyboardMarkup()
            keyboard.row(InlineKeyboardButton("✅Подтвердить", callback_data=f"strs;{username};{count}"))
            keyboard.row(InlineKeyboardButton("↩️Отмена", callback_data="tgCancel"))
            bot.edit_message_text(f"""<b>
⭐️ Пoкyпка звёзд
                                  
🏦 Баланс: <code>{data[1]}$</code>

👤 Получатель: <a href="https://t.me/{username}">{name}</a>
💎 Количество: <code>{count}</code>
💰 Цена: <code>{round(count * 0.015 * TG_SERVICE_EXTRA, 2)}</code>

🚀 Подтвердите пoкyпку звёзд</b>""", message.chat.id, old_id, reply_markup=keyboard)
    except Exception as e:
        msg = bot.edit_message_text(f"""<b>💫 Укажите количество звёзд для {name}:

Минимум: 50 звезд
Максимум: 1 000 000 звезд
                                    
Вы ввели не число</b>""", message.chat.id, old_id, reply_markup=keyboard)
        bot.register_next_step_handler(msg, starscounthandler, msg.id, username, name)
    try:
        bot.delete_message(message.chat.id, message.id)
    except:
        ...
        



def starsuserInfo(message, old_id):
    data = get_data(message.from_user.id)
    username = message.text.strip()
    url = "https://tg.parssms.info/v1/stars/search"
    payload = json.dumps({
 "query": username,
 "quantity": "50"
})
    headers = {
 'Content-Type': 'application/json',
 'api-key': api_key
}
    response = requests.post(url, headers=headers, data=payload).json()
    if not response['ok']:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("⬅️Отмена", callback_data="tgCancel"))
        msg = bot.edit_message_text(f"""<b>⭐️ Telegram Stars

• Стоимость одной звезды: 1.80₽

• Отправьте @username получателя, для которого хотите купить звёзды (звезды поступят автоматически в течение 20 секунд)
                                    
Пользователь не найден!</b>""", message.chat.id, old_id, reply_markup=keyboard)
        bot.register_next_step_handler(msg, starsuserInfo, msg.id)
    else:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("⬅️Отмена", callback_data="tgCancel"))
        msg = bot.edit_message_text(f"""<b>💫 Укажите количество звёзд для {response['found']['name']}

Минимум: 50 звезд
Максимум: 1 000 000 звезд</b>""", message.chat.id, old_id, reply_markup=keyboard)
        bot.register_next_step_handler(msg, starscounthandler, msg.id, username, response['found']['name'])
    try:
        bot.delete_message(message.chat.id, message.id)
    except:
        ...


@bot.callback_query_handler(lambda call: call.data == "tgCancel")
def tgCancelHandler(call: CallbackQuery):
    bot.clear_step_handler(call.message)
    catalogs_handler(call)


@bot.callback_query_handler(lambda call: call.data.startswith("buy_"))
def submit_handler(call: CallbackQuery):
    data = get_data(call.from_user.id)
    shortname = call.data.replace("buy_", "")
    match shortname:
        case "fiz_rf":
            if data[1] < 2.5:
                bot.answer_callback_query(call.id, "На вашем балансе недостаточно средст(\n\nПополните баланс и попробуйте снова!", True)
            else:
                sessions = listdir("sessions")
                if sessions == []:
                    bot.answer_callback_query(call.id, "Прямо сейчас в боте нет сессий! Попробуйте снова позже, или обратитесь к администратору", True)
                    bot.send_message(OWNER_ID, "<b>В боте закончились сессии!\nДобавь еще через команду /add_session</b>")
                else:
                    session_name = sessions[0].replace(".session", "")
                    keyboard = InlineKeyboardMarkup()
                    keyboard.row(InlineKeyboardButton("📥Получить код", callback_data="fiz_rf_code"))
                    with con:
                        cursor = con.cursor()
                        cursor.execute("INSERT INTO codes VALUES(?,?,?)", (session_name, time(), None))
                    Thread(target=system, args=(f"python session_message_waiter.py {session_name}",)).start()
                    bot.edit_message_text(f"""<b>✈️ Покупка Telegram accounts

🏦 Баланс: <code>{data[1]}$</code>

👤 Получатель: @{call.from_user.username}
📱 Номер телефона: <code>{session_name}</code>
💰 Цена: <code>2.5$</code>

🚀Чтобы получить код для входа в аккаунт нажмите кнопку ниже!</b>""", call.message.chat.id, call.message.id, reply_markup=keyboard)
        case "premium":
            keyboard = InlineKeyboardMarkup()
            keyboard.row(InlineKeyboardButton("⬅️Отмена", callback_data="tgCancel"))
            msg = bot.edit_message_text(f"""<b>💎 Telegram Premium          
                             
• 🎁 3/6/12 месяцев – автоматическая отправка подарком.                                        

• Отправьте @username получателя, которому хотите подарить премиум (премиум поступит автоматически, в течение 20 секунд)</b>""", call.message.chat.id, call.message.id, reply_markup=keyboard)
            bot.register_next_step_handler(msg, premiumuserInfo, msg.id)
        case "stars":
            keyboard = InlineKeyboardMarkup()
            keyboard.row(InlineKeyboardButton("⬅️Отмена", callback_data="tgCancel"))
            msg = bot.edit_message_text(f"""<b>⭐️ Telegram Stars

• Стоимость одной звезды: 1.80₽

• Отправьте @username получателя, для которого хотите купить звёзды (звезды поступят автоматически, в течение 20 секунд)</b>""", call.message.chat.id, call.message.id, reply_markup=keyboard)
            bot.register_next_step_handler(msg, starsuserInfo, msg.id)
        case shortname:
            with con:
                cursor = con.cursor()
                cursor.execute("SELECT * FROM products WHERE shortname=?", (shortname,))
                product_info = cursor.fetchone()
                if data[1] < product_info[5]:
                    bot.answer_callback_query(call.id, "На вашем балансе недостаточно средст(\n\nПополните баланс и попробуйте снова!", True)
                else:
                    cursor.execute("UPDATE users SET balance=balance-? WHERE id=?", (product_info[5], data[0]))
                    bot.edit_message_text(f"<b>🚀 Товар: {product_info[1]} | {product_info[5]}$\n🎁 Описание: {product_info[2]}\nПерешлите это сообщение администратору, чтобы получить ваш заказ</b>", call.message.chat.id, call.message.id, reply_markup=buyed_shit_kb())
                    bot.send_message(OWNER_ID, f'Пользователь {call.from_user.id} заказал и оплатил {product_info[1]}', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Пользователь", f'tg://user?id={call.from_user.id}')))



@bot.callback_query_handler(CqueryFunc(*get_categories()))
def categories_handler(call: CallbackQuery):
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM products WHERE category=?", (call.data,))
        products = cursor.fetchall()
    keyboard = InlineKeyboardMarkup()
    for product in products:
        keyboard.row(InlineKeyboardButton(product[1], callback_data=f"{product[0]}"))
    keyboard.row(InlineKeyboardButton("⬅️Вернуться", callback_data="start"))
    bot.edit_message_text(f"<b>Товары из категории {call.data}\n\nНажмите на название товара чтобы получить полное описание</b>", call.message.chat.id, call.message.id, reply_markup=keyboard)
    


@bot.callback_query_handler(CqueryFunc("catalogs"))
def catalogs_handler(call: CallbackQuery):
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    bot.edit_message_text("""<b>🚀 Ассортимент услуг
Выберите один из вариантов

Для продолжения нажмите на нужную вам услугу</b>""", call.message.chat.id, call.message.id, reply_markup=catalog_kb(products))



@bot.callback_query_handler(CqueryFunc("start"))
@bot.message_handler(['start'])
def start_handler(message: Message):
    data = get_data(message.from_user.id)
    if not data[5]:
        return bot.send_message(message.chat.id, """<b>🎩 Для начала пользования бота вам необходимо ознакомиться с пользовательским соглашением:
кнопки</b>""", reply_markup=user_agreement_kb())
    try:
        ref = int(message.text.replace("/start ", ""))
        with con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM users WHERE id=?", (ref,))
            if cursor.fetchone() != []:
                cursor.execute("UPDATE users SET ref=? WHERE id=?", (ref, message.from_user.id))
                bot.send_message(ref, f"<b>Пользователь присоединился по вашей ссылке!\n\nтеперь вы получаете {int(REF_PERCENT * 100)}% с его пополнений!</b>")
    except:
        ...
    if type(message) is Message:
        bot.send_sticker(message.chat.id, "CAACAgEAAxkBAAEOhZloKyyJcJTZUxqQ6s1UqheNX27BewACGwMAArAHGESRLvZwzZJ9sjYE")
        bot.send_message(message.chat.id, """<b>🚀 Добро пожаловать в Trip Shop!

📌 Вы попали в <u>лучший</u> цифровой магазин, ведь на данный момент мы являемся <u>лидером</u> среди конкурентов. У нас самые низкие цены, отзывчивая техническая поддержка, качественные товары, актуальность и многое другое.</b>""", reply_markup=start_kb())
    else:
        bot.edit_message_text("""<b>🚀 Добро пожаловать в Trip Shop!

📌 Вы попали в <u>лучший</u> цифровой магазин, ведь на данный момент мы являемся <u>лидером</u> среди конкурентов. У нас самые низкие цены, отзывчивая техническая поддержка, качественные товары, актуальность и многое другое.</b>""", message.message.chat.id, message.message.id, reply_markup=start_kb())


@bot.callback_query_handler(CqueryFunc("profile"))
def profile(call: CallbackQuery):
    data = get_data(call.from_user.id)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE ref=?", (call.from_user.id,))
        ref_count = len(cur.fetchall())
    text = f"""<b>
👤Ваш профиль:
💎Юзер: <b>@{call.from_user.username}</b>
🆔ID: <code>{call.from_user.id}</code>
💰Баланс: <code>${data[1]}</code>
💵Всего пополнено: <code>{data[2]}</code>
📌Дата регистрации: <code>{ctime(data[3])}</code>
👥Рефералов: <code>{ref_count}</code>
</b>"""
    bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=profile_kb())


@bot.callback_query_handler(CqueryFunc("balance"))
def balance_handler(call: CallbackQuery):
    bot.edit_message_text("<b>💰 Выберите способ пополнения</b>", call.message.chat.id, call.message.id, reply_markup=balance_kb())


@bot.callback_query_handler(CqueryFunc("check_payment"))
def check_payment_handler(call:CallbackQuery):
    txt = call.message.text.split("\n")
    payment_method = txt[0].replace("Платежная система: ", "")
    invoice_id = txt[1].replace("Айди платежа: ", "")
    amount = float(txt[2].replace("Сумма: ", ""))
    data = get_data(call.from_user.id)
    if payment_method != "cryptopay":
        invoice = CrystalPay.getInvoice(invoice_id)
        if invoice['state'] == "notpayed":
            bot.answer_callback_query(call.id, "Счет пока что не оплачен!")
        else:
            bot.send_message(OWNER_ID, f"<b>{call.from_user.username} пополнил баланс на {amount}</b>")
            with con:
                cursor = con.cursor()
                if not data[4] is None:
                    cursor.execute("UPDATE users SET balance=balance+? AND deposit=deposit+? WHERE id=?", (amount * REF_PERCENT, amount * REF_PERCENT, data[4]))
                    try: bot.send_message(data[4], f"<b>Ваш реферал пополнил баланс на {amount}$\n\nНа ваш баланс зачислено {amount * REF_PERCENT}$</b>")
                    except: ...
                cursor.execute("UPDATE users SET balance=balance+? WHERE id=?", (amount, call.from_user.id))
                bot.answer_callback_query(call.id, "Успешное пополнение!\nПриятных покупок")
                profile(call)
    else:
        invoice = CryptoPay.get_invoice(invoice_id)
        if invoice['status'] != "paid":
            bot.answer_callback_query(call.id, "Счет пока что не оплачен!")
        else:
            bot.send_message(OWNER_ID, f"<b>{call.from_user.username} пополнил баланс на {amount}</b>")
            with con:
                cursor = con.cursor()
                if not data[4] is None:
                    cursor.execute("UPDATE users SET balance=balance+? AND deposit=deposit+? WHERE id=?", (amount * REF_PERCENT, amount * REF_PERCENT, data[4]))
                    try: bot.send_message(data[4], f"<b>Ваш реферал пополнил баланс на {amount}$\n\nНа ваш баланс зачислено {amount * REF_PERCENT}$</b>")
                    except: ...
                cursor.execute("UPDATE users SET balance=balance+? WHERE id=?", (amount, call.from_user.id))
                bot.answer_callback_query(call.id, "Успешное пополнение!\nПриятных покупок")
                profile(call)


def amount_getter(message, old_message_id, payment_method):
    try:
        bot.delete_message(message.chat.id, message.id)
    except:
        ...
    try:
        amount = float(message.text.strip())
        if amount < MIN_DEPOSIT:
            msg = bot.edit_message_text(f"<b>Введите сумму пополнения</b>\nМинимальная сумма: {MIN_DEPOSIT}", message.chat.id, old_message_id)
            bot.register_next_step_handler(msg, amount_getter, old_message_id, payment_method)
        else:
            if payment_method != "cryptopay":
                invoice = CrystalPay.createInvoice(amount, redirect_url=f"https://t.me/({bot.get_me().username})")
                invoice_id = invoice['id']
                pay_url = invoice['url']
            else:
                invoice = CryptoPay.create_invoice(amount)
                invoice_id = invoice['invoice_id']
                pay_url = invoice['pay_url']
            keyboard = InlineKeyboardMarkup()
            keyboard.row(InlineKeyboardButton("💸Оплатить", pay_url))
            keyboard.row(InlineKeyboardButton("🔄Проверить оплату", callback_data="check_payment"))
            bot.edit_message_text(f"<b>Платежная система: {payment_method}\nАйди платежа: {invoice_id}\nСумма: {amount}\n\nОплатите счет по ссылке ниже, чтобы пополнить баланс!</b>", message.chat.id, old_message_id, reply_markup=keyboard)
    except:
        msg = bot.edit_message_text("<b>Введите сумму пополнения</b>\nВведите число!", message.chat.id, old_message_id)
        bot.register_next_step_handler(msg, amount_getter, old_message_id, payment_method)
    

@bot.callback_query_handler(CqueryFunc("cryptopay", "crystalpay"))
def payment_method_handler(call: CallbackQuery):
    msg = bot.edit_message_text("<b>Введите сумму пополнения</b>", call.message.chat.id, call.message.id, reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Отмена", callback_data="balance_cancel")))
    bot.register_next_step_handler(msg, amount_getter, msg.id, call.data)


@bot.callback_query_handler(CqueryFunc("balance_cancel"))
def balance_cancel_handler(call: CallbackQuery):
    bot.clear_step_handler(call.message)
    balance_handler(call)


print(bot.get_me())
bot.infinity_polling()