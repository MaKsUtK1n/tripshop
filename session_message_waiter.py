from pyrogram import Client, filters
from sys import argv
from time import sleep
from sqlite3 import Connection
from threading import Thread
from os import rename


session_name = argv[1]
is_get_code = False
rename(f"sessions/{session_name}.session", f"working_sessions/{session_name}.session")
app = Client(f"working_sessions/{session_name}", 25389095, "a715da4e82e7a2bab63fef6364c62596")
app.connect()
print(app.get_me())
app.disconnect()
con = Connection("db.db", isolation_level=None, check_same_thread=False)



@app.on_message(filters.create(lambda *m: m[2].from_user.id == 777000))
def code_handler(client, message):
    global is_get_code
    code = message.text.replace("Код для входа в Telegram: ", "").replace(""". Не давайте код никому, даже если его требуют от имени Telegram!

❗️Этот код используется для входа в Ваш аккаунт в Telegram. Он не может быть использован для чего-либо ещё. 

Если Вы не запрашивали код для входа, проигнорируйте это сообщение.""", "")
    print(message.text)
    with con:
        cursor = con.cursor()
        cursor.execute("UPDATE codes SET code=? WHERE session_name=?", (code, session_name))        
    is_get_code = True


def waiter():
    for _ in range(578):
        if is_get_code:
            try:
                app.stop()
                app.disconnect()
            except:
                ...
            exit()
        sleep(1)
    rename(f"working_sessions/{session_name}.session",f"sessions/{session_name}.session")
    exit()


Thread(target=waiter).start()
app.run()