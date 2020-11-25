import telegram, datetime, telegram.ext, logging, random, psutil, os, subprocess, re, pandas
import getpass, json
from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler, CallbackContext, Updater
from time import sleep

json_setup = json.loads(open("setup.json").read())
updater = telegram.ext.Updater(token=json_setup['token'], use_context=True)
dispatcher = updater.dispatcher
path = os.path.dirname(os.path.realpath(__file__))
pid = str(os.getpid())
pidfile = "{}/helper/aquabot.pid".format(path)

if os.path.exists("log/") == False:
    os.mkdir("log/")

def greet():
    now = datetime.datetime.now()
    jam = now.strftime("%H:%M:%S")
    if (re.compile(r"0\d\:\d\d:\d\d").search(jam)):
        return("Pagi")
    elif (re.compile(r"1[01234]\:\d\d:\d\d").search(jam)):
        return("Siang")
    elif (re.compile(r"1[5678]\:\d\d:\d\d").search(jam)):
        return("Sore")
    else:
        return("Malam")
    print(greet())

def text(update, context):
    jawaban = [
        "Maaf, Aqua bukanlah bot interaktif.",
        "申し訳ありませんが、Aquaはインタラクティブなボットではありません。",
        "Sorry, Aqua is not an interactive bot.",
        "Entschuldigung, Aqua ist kein interaktiver Bot.",
        "Извините, Aqua не интерактивный бот."
    ]
    context.bot.send_message(update.effective_message.chat.id, text=jawaban[random.randrange(len(jawaban))])

def command(update = Update, context = CallbackContext) -> None:
    now = datetime.datetime.now()
    jam = now.strftime("%H:%M:%S")
    full = now.strftime("%Y/%m/%d")
    file_json = open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(getpass.getuser(), datetime.datetime.now().strftime("%Y-%m"), datetime.datetime.now().strftime("%d")))
    data = json.loads(file_json.read())
    convert = pandas.DataFrame(data["{}".format(full)])
    command = update.message.text
    chat_type = update.message.chat.type
    username = update.message.from_user.username
    chat_id = update.message.from_user.id

    if command == "/start":
        pesan = "Hai, aku adalah <b>Aqua</b>\n"
        pesan += "Bot yang dibuat untuk membantu pengguna sekalian dalam pengoprasian aquabellus\n\n"
        pesan += "Untuk memanggilku, silahkan kirim perintah <code>/aqua</code>"
        context.bot.send_message(update.effective_message.chat.id, pesan, parse_mode="HTML")

    elif command == "/aqua":
        jawaban = "Sekarang jam {}\n-------------------------\n\n".format(jam)
        pesan = [
            "Kenapa ?",
            "Aku padamu {}".format(username),
            "Ikan hiu makan permen\nHadir 😎",
            "Boo",
            "Disini"
        ]
        pesan_khusus = [
            "Loh, belum tidur ?",
            "Udah malem padahal",
            "Waktunya istirahat 😡",
            "Ngantuk 😭",
            "Hadiiirrrr 😵️"
        ]
        if (re.compile(r"2\d:\d\d:\d\d").search(jam)):
            context.bot.send_message(update.effective_message.chat.id, jawaban + pesan_khusus[random.randrange(len(pesan_khusus))], parse_mode="HTML")
        else:
            context.bot.send_message(update.effective_message.chat.id, jawaban + pesan[random.randrange(len(pesan))], parse_mode="HTML")

    elif command == "/last":
        pesan = "<b>{}</b>\n\n".format(full)
        context.bot.send_message(update.effective_message.chat.id, pesan + "{}".format(convert.tail(1)), parse_mode="HTML")

    elif command == "/full":
        pesan = "<b>{}</b>\n\n".format(full)
        context.bot.send_message(update.effective_message.chat.id, pesan + "{}".format(convert), parse_mode="HTML")

    elif command == "/about":
        pesan = "Aku perkenalan lagi yaa\n"
        pesan += "Namaku adalah <b>Aqua</b>, tapi bukan Aqua galon 😡\n\n"
        pesan += "Aku dibuat untuk membantu kalian semua, dalam pengoprasian produk-produk aquabellus\n"
        pesan += "Berikut adalah list perintah yang bisa aku kerjakan :\n"
        pesan += "<code>/last</code> -> Menampilkan hasil dump terakhir\n"
        pesan += "<code>/full</code> -> Menampilkan hasil dump secara keseluruhan\n"
        pesan += "<code>/id</code> -> Menampilkan Chat ID\n"
        pesan += "<code>/status</code> -> Menampilkan status\n\n"
        pesan += "Untuk informasi lebih lanjut silahkan kunjungi <a href='https://github.com/aquabellus'>tautan ini</a>\n\n"
        pesan += "Terima kasih 😊   -aquabellus"
        context.bot.send_message(update.effective_message.chat.id, pesan, parse_mode="HTML")

    elif command == "/id":
        pesan = "Hai {}\nSelamat {}\n\nChat ID kamu adalah : {}".format(username, greet(), chat_id)
        if chat_type == "private":
            """DOES NOTHING"""
        elif chat_type == "supergroup":
            pesan += "\nChat ID grup ini adalah : {}".format(update.effective_message.chat.id)
        else:
            pesan += "\nChat ID {} ini adalah : {}".format(chat_type, update.effective_message.chat.id)
        context.bot.send_message(update.effective_message.chat.id, pesan, parse_mode="HTML")

    elif command == "/config":
        buka = json.load(open("setup.json", "r"))
        pesan = "<b>Konfigurasi</b> :\n\n"
        pesan += "host : <code>{}</code>\n".format(buka["host"])
        pesan += "user : <code>{}</code>\n".format(buka["user"])
        pesan += "passwd : <code>{}</code>\n".format("*"*3)
        pesan += "database : <code>{}</code>\n".format(buka["database"])
        pesan += "token : <code>{}</code>\n".format(re.compile(r"\d+\:").search(buka["token"]).group() + '*'*3)
        pesan += "chatid : <code>{}</code>".format(buka["chatid"])
        context.bot.send_message(update.effective_message.chat.id, pesan, "HTML")

def reboot(update = Update, context = CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="reboot")
        ],
        [
            InlineKeyboardButton("Nevermind", callback_data="nmind")
        ]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)
    pesan = "Are you sure want to reboot this bot ?"
    update.message.reply_text(pesan, reply_markup=inline_markup)

def setup(update = Update, context = CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Hehe 😅", callback_data="hehe"),
            InlineKeyboardButton("Entah", callback_data="entah"),
            InlineKeyboardButton("100%", callback_data="100")
        ],
            [InlineKeyboardButton("Enggak", callback_data="enggak")],
            [InlineKeyboardButton("Gajadi", callback_data="gajadi")],
            [InlineKeyboardButton("Anu", callback_data="anu")]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)
    pesan = "<b>Mohon Diperhatikan</b>\n\n"
    pesan += "Perintah ini hanya digunakan sekali saja, yakni pada saat awal konfigurasi\n"
    pesan += "Apabila {} tidak yakin dengan apa yang kamu lakukan, mohon untuk membatalkan perintah\n".format(update.message.from_user.username)
    pesan += "Q = Kenapa ?\n"
    pesan += "A = Karena perintah ini berfungsi untuk membuat DataBase dan Tabel <b>(Baru)</b>, dan dapat menyebabkan error apabila perintah ini dilaksanakan 2 kali.\n\n\n"
    pesan += "Apakah Kamu Yakin Untuk Melanjutkan Perintah Ini ?"
    update.message.reply_text(pesan, parse_mode="HTML", reply_markup=inline_markup)

def log(update = Update, context = CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("aquabot", callback_data="aquabot"),
            InlineKeyboardButton("aquastart", callback_data="aquastart"),
            InlineKeyboardButton("aquasetup", callback_data="aquasetup")
        ]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)
    pesan = "Silahkan pilih log yang ingin ditampilkan"
    update.message.reply_text(pesan, reply_markup=inline_markup)

def status(update = Update, context = CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Mulai Ulang", callback_data="mulai"),
            InlineKeyboardButton("Matikan", callback_data="matikan")
        ]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)
    run = bool(check())
    pesan = "<b>Script Tidak Terdeteksi !!!</b>\n\n"
    if run == False:
        update.message.reply_text(pesan, parse_mode="HTML", reply_markup=inline_markup)
    else:
        update.message.reply_text("Script Sudah Berjalan", parse_mode="HTML", reply_markup=inline_markup)
        
def notif(status):
    now = datetime.datetime.now()
    jam = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    Aqua = telegram.Bot(json_setup["token"])
    pesan = [
        "Status <b>{}</b> Terdeteksi Pada Pukul <b>{}</b>".format(status, jam),
        "Lapor, Aqua Menerima Sinyal <b>{}</b> Pada Pukul <b>{}</b>".format(status, jam),
        "WiWuWiWu, Sinyal <b>{}</b> Tertangkap Pada Pukul <b>{}</b>".format(status, jam),
        "Aqua Datang Dengan Membawa Berita <b>{}</b> Yang Terjadi Pada Pukul <b>{}</b>".format(status, jam)
    ]
    if status == "mati":
        Aqua.sendMessage(json_setup["chatid"], "Script Tidak Berjalan, Terdeteksi pada pukul {}".format(jam), parse_mode="HTML")
    else:
        Aqua.sendMessage(json_setup["chatid"], pesan[random.randrange(len(pesan))], parse_mode="HTML")

def ready():
    Aqua = telegram.Bot(json_setup["token"])
    Aqua.sendMessage(json_setup["chatid"], "Aqua Ready")

def alert():
    Aqua = telegram.Bot(json_setup["token"])
    pesan = [
        "Wiwuu Wiwuu Wiwuu, Aqua Mendeteksi kemungkinan Banjir",
        "Bahayaaa, Mohon Segera Cek TKP-nya Kakak !!!",
        "Ayo Segera Cek Kakak"
    ]
    Aqua.sendMessage(json_setup["chatid"], pesan[random.randrange(len(pesan))])

def pressed():
    Aqua = telegram.Bot(json_setup["token"])
    pesan = [
        "Tombol sudah ditekaaaan terimakasih",
        "Notifikasi telah dimatikan kakak",
        "Terimakasih atas bantuannya XD"
    ]
    Aqua.sendMessage(json_setup["chatid"], pesan[random.randrange(len(pesan))])

def check():
    for process in psutil.process_iter():
        if process.cmdline() == ['python3', 'aquastart.py']:
            return(True)
    return(False)

def button(update: Update , context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == "mulai":
        keyboard = [
            [
                InlineKeyboardButton("Iyalah", callback_data="iya"),
                InlineKeyboardButton("Eh apa ?", callback_data="apa"),
                InlineKeyboardButton("Ini apa sih ?", callback_data="apasih")
            ],
            [
                InlineKeyboardButton("Enggak kok", callback_data="enggakkok")
            ]
        ]
        inline_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Kamu yakin ? 😌️", reply_markup=inline_markup)

    elif query.data == "matikan":
        keyboard = [
            [
                InlineKeyboardButton("Ragu", callback_data="ragu"),
                InlineKeyboardButton("Umm", callback_data="umm"),
                InlineKeyboardButton("Enggak deh", callback_data="enggakdeh")
            ],
            [
                InlineKeyboardButton("Oh tentu saja", callback_data="tentu")
            ]
        ]
        inline_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Kamu serius ?", reply_markup=inline_markup)
        
    elif query.data == "reboot":
        query.edit_message_text("Rebooting bot ...")
        if os.path.exists("helper/aquabot.pid"):
            os.system("kill {}".format(open("helper/aquabot.pid").read()))
        else:
            pesan = "Helper file not found\n\nOperation aborted !!!"
            context.bot.send_message(update.effective_message.chat.id, pesan, parse_mode="HTML")

    elif query.data == "tentu":
        query.edit_message_text("Menghentikan Script ...")
        if check() == True:
            if os.path.exists("helper/aquastart.pid"):
                try:
                    os.system("kill {}".format(open("helper/aquastart.pid").read()))
                    sleep(1)
                finally:
                    if check() == False:
                        context.bot.send_message(update.effective_message.chat.id, "Script Berhasil Dihentikan")
                    else:
                        context.bot.send_message(update.effective_message.chat.id, "Gagal Menghentikan Script")
            else:
                pesan = "File Daemon Tidak Ditemukan\nGagal Menghentikan Script"
                context.bot.send_message(update.effective_message.chat.id, pesan, parse_mode="HTML")
        else:
            context.bot.send_message(update.effective_message.chat.id, "Script Sudah Berhenti.")

    elif query.data == "iya":
        query.edit_message_text(text="Memulai Ulang Script ...")
        if check() == False:
            if os.path.exists("aquastart.py"):
                try:
                    os.system("lxterminal -e python3 aquastart.py")
                    sleep(1)
                finally:
                    if check() == True:
                        context.bot.send_message(update.effective_message.chat.id, "Script Berhasil Dimulai Ulang")
                    else:
                        context.bot.send_message(update.effective_message.chat.id, "Script Gagal Dimulai Ulang")
            else:
                pesan = "File Tidak Ada\nGagal Memulai Ulang !!!"
                context.bot.send_message(update.effective_message.chat.id, pesan)
        else:
            context.bot.send_message(update.effective_message.chat.id, "Script Sudah Berjalan.")

    elif query.data == "100":
        if os.path.exists("aquasetup.py"):
            try:
                os.system("lxterminal -e python3 aquasetup.py")
                sleep(1)
            finally:
                query.edit_message_text("Script berhasil dijalankan\nMohon cek log untuk detail lebih lanjut.")
        else:
            query.edit_message_text("File tidak ditemukan !!!")

    elif query.data == "aquabot":
        if os.path.exists("log/aquabot.log"):
            log = open("log/aquabot.log").read()
            context.bot.send_message(update.effective_message.chat.id, "<b>aquabot.log</b>\n\n" + log, "HTML")
        else:
            context.bot.send_message(update.effective_message.chat.id, "File tidak ditemukan")
    elif query.data == "aquastart":
        if os.path.exists("log/aquastart.log"):
            log = open("log/aquastart.log").read()
            context.bot.send_message(update.effective_message.chat.id, "<b>aquastart.log</b>\n\n" + log, "HTML")
        else:
            context.bot.send_message(update.effective_message.chat.id, "File tidak ditemukan")
    elif query.data == "aquasetup":
        if os.path.exists("log/aquasetup.log"):
            log = open("log/aquasetup.log").read()
            context.bot.send_message(update.effective_message.chat.id, "<b>aquasetup.log</b>\n\n" + log, "HTML")
        else:
            context.bot.send_message(update.effective_message.chat.id, "File tidak ditemukan")
    else:
        pesan = [
            "Dasar",
            "Plin-plan",
            "Nyusahin aja",
            "Sabar, gaboleh ngatain 😊"
        ]
        query.edit_message_text(pesan[random.randrange(len(pesan))])

def minute_count():
    a = datetime.datetime.now().strftime("%M")
    a = int(a) + 15
    if a >= 60:
        a -= 60
    return(a)

text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(CommandHandler("setup", setup))
dispatcher.add_handler(CommandHandler("log", log))
dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(CommandHandler("reboot", reboot))
command_handler = MessageHandler(Filters.command, command)
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(command_handler)
dispatcher.add_handler(text_handler)

if os.path.exists("helper/") == False:
    os.mkdir("helper/")
if os.path.isfile(pidfile):
    print("{} Sudah Tersedia, Menulis Ulang ...".format(pidfile))
open(pidfile, 'w').write(pid)


if __name__ == "__main__":
    logging.basicConfig(filename='log/aquabot.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    try:
        updater.start_polling()
    except:
        logging.warning('This will get logged to a file')
    finally:
        ready()
        print("Bot Started")
        a = 0
        while True:
            now_minute = datetime.datetime.now().strftime("%M")
            int_min = int(now_minute)
            if check() == False:
                if a == 0:
                    notif("mati")
                    a = minute_count()
                elif int_min == a:
                    notif("mati")
                    a = minute_count()
            else:
                a = 0
            print("##########")
            print("aquabot.py")
            print("a telegram bot script")
            print("")
            print("")
            if a == 0:
                print("Script berjalan")
                print("Notifikasi akan dikirimkan seketika apabila script berhenti")
            else:
                print("Script berhenti")
                print("Script akan dicek ulang pada menit ke {}".format(a))
            if datetime.datetime.now().strftime("%H%M") == "0005":
                if os.path.exists("helper/aquabot.pid"):
                    os.system("kill {}".format(open("helper/aquabot.pid").read()))
            sleep(1)
            os.system("clear")