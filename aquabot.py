import telegram, datetime, logging, psutil, os, re, signal
import getpass, json
import json.decoder as jsonError
from numpy import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler, CallbackContext
from time import sleep
from urllib import request
from functools import wraps

#Konfigurasi untuk menyimpan log
logging.basicConfig(filename='log/aqualog.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

#Penyerhanaan variabel 
json_setup = json.loads(open("setup.json").read())  #Membuka dan membaca file .json
updater = telegram.ext.Updater(token=json_setup['token'], use_context=True) #Set token telegrambot
dispatcher = updater.dispatcher #Konfigurasi dispatcher
#Untuk detail lebih lanjut mengenai telegrambot silahkan kunjungi situs resmi telegrambot dan python-for-telegram

#Melakukan pengecekan pada folder ~../log, apabila folder tidak ada maka akan dibuat folder baru
if os.path.exists("log/") == False:
    os.mkdir("log/")

#Fungsi untuk menentukan sekarang Pagi/Siang/Sore/Malam
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

def typing(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(update.effective_message.chat.id, action=telegram.ChatAction.TYPING)
        return func(update, context, *args, **kwargs)
    return command_func

def upload(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(update.effective_message.chat.id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
        return func(update, context, *args, **kwargs)
    return command_func

def chatbot(pesan):
    saring = re.sub(r" ", "+", pesan)
    jawaban = request.urlopen("https://chatbot-indo.herokuapp.com/get/{}".format(saring))
    urai = json.loads(jawaban.read())
    return(urai["msg"])

#Fungsi agar Aqua membalas pesan berupa text
@typing
def text(update, context):
    jawaban = chatbot(update.effective_message.text)
    context.bot.send_message(update.effective_message.chat.id, text=jawaban)

#Fungsi perintah yang dapat dijalankan oleh Aqua
@typing
def command(update = Update, context = CallbackContext) -> None:
    now = datetime.datetime.now()   #Variabel untuk menunjukkan date/time sekarang
    jam = now.strftime("%H:%M:%S")  #Variabel untuk mengambil saat sekarang berdasarkan format yang telah ditentukan
    command = update.message.text   #Mengambil perintah yang dikirimkan oleh pengguna
    chat_type = update.message.chat.type    #Mengambil tipe chat
    username = update.message.from_user.username    #Mengambil username pengguna
    chat_id = update.message.from_user.id   #Mengambil chat id pengguna

    #Fungsi untuk menangani perintah
    if command == "/start": #Apabila perintah /start diterima maka lakukan kode dibawah
        pesan = "Hai, aku adalah <b>Aqua</b>\n" #Penyerhanaan variabel pesan
        pesan += "Bot yang dibuat untuk membantu pengguna sekalian dalam pengoprasian aquabellus\n\n"   #Menambah variabel pesan
        pesan += "Untuk memanggilku, silahkan kirim perintah <code>/aqua</code>\n\n"
        pesan += "Terus, untuk hal-hal lain coba pake perintah <code>/about</code>"
        context.bot.send_message(update.effective_message.chat.id, pesan, parse_mode="HTML")    #Mengambil module kirim pesan, kemudian mendapatkan chat id pengguna, kirim pesan dengan variabel pesan, gunakan metode parsing html

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
        if (re.compile(r"2\d:\d\d:\d\d").search(jam)):  #Menggunakan pola regex untuk mendapatkan value 2n:nn:nn
            context.bot.send_message(update.effective_message.chat.id, jawaban + pesan_khusus[int(random.randint(0, len(pesan_khusus)))], parse_mode="HTML")
        else:   #Apabila hasil diatas tidak ditemukan maka lakukan perintah dibawah
            context.bot.send_message(update.effective_message.chat.id, jawaban + pesan[int(random.randint(0, len(pesan)))], parse_mode="HTML")

    elif command == "/about":
        pesan = "Aku perkenalan lagi yaa\n"
        pesan += "Namaku adalah <b>Aqua</b>, tapi bukan Aqua galon 😡\n\n"
        pesan += "Aku dibuat untuk membantu kalian semua, dalam pengoprasian produk-produk aquabellus\n"
        pesan += "Berikut adalah list perintah yang bisa aku kerjakan :\n"
        pesan += "<code>/last</code> -> Menampilkan hasil dump terakhir\n"
        pesan += "<code>/full</code> -> Mengirimkan hasil dump pada hari ini dalam bentuk file\n"
        pesan += "<code>/id</code> -> Menampilkan Chat ID\n"
        pesan += "<code>/status</code> -> Menampilkan status\n\n"
        pesan += "Untuk informasi lebih lanjut silahkan kunjungi <a href='https://github.com/aquabellus'>tautan ini</a>\n\n"
        pesan += "Terima kasih 😊   -aquabellus"
        context.bot.send_message(update.effective_message.chat.id, pesan, parse_mode="HTML")

    elif command == "/id":
        pesan = "Hai {}\nSelamat {}\n\nChat ID kamu adalah : <code>{}</code>".format(username, greet(), chat_id)
        if chat_type == "private":
            pesan += "\nAku juga bisa kok nampilin Chat ID grup kamu. 😊"
        elif chat_type == "supergroup":
            pesan += "\nChat ID grup ini adalah : <code>{}</code>".format(update.effective_message.chat.id)
        else:
            pesan += "\nChat ID {} ini adalah : <code>{}</code>".format(chat_type, update.effective_message.chat.id)
        context.bot.send_message(update.effective_message.chat.id, pesan, parse_mode="HTML")

    elif command == "/config":
        buka = json.load(open("setup.json", "r"))
        pesan = "<b>Konfigurasi</b> :\n\n"
        pesan += "host : <code>{}</code>\n".format(buka["host"])
        pesan += "user : <code>{}</code>\n".format(buka["user"])
        pesan += "passwd : <code>{}</code>\n".format("*"*3)
        pesan += "database : <code>{}</code>\n".format(buka["database"])
        pesan += "token : <code>{}</code>\n".format(re.compile(r"\d+\:").search(buka["token"]).group() + '*'*3)
        pesan += "chatid : <code>{}</code>".format(re.search(r"\d{5}", buka["chatid"]).group() + '*'*3)
        context.bot.send_message(update.effective_message.chat.id, pesan, "HTML")

#Fungsi untuk mengirimkan data hasil dump keseluruhan dalam bentuk file
@upload
def full(update = Update, context = CallbackContext):
    try:
        buka = open("/home/{}/Documents/BoxDump.d/BoxDump.json".format(getpass.getuser()))
        json.loads(buka.read())
    except FileNotFoundError:
        return(context.bot.send_message(update.effective_message.chat.id, "File tidak ditemukan"))
    except (AttributeError, jsonError.JSONDecodeError):
        return(context.bot.send_message(update.effective_message.chat.id, "File tidak dapat dibaca"))
    file_json = open("/home/{}/Documents/BoxDump.d/BoxDump.json".format(getpass.getuser()), "rb")
    context.bot.send_document(update.effective_message.chat.id, document=file_json) #Modul untuk mengirimkan dokumen

#Fungsi untuk mengirimkan data terakhir hasil dump hari ini
@typing
def last(update = Update, context = CallbackContext):
    try:
        buka = open("/home/{}/Documents/BoxDump.d/BoxDump.json".format(getpass.getuser()))
        json.loads(buka.read())
    except FileNotFoundError:
        return(context.bot.send_message(update.effective_message.chat.id, "File tidak ditemukan"))
    except (AttributeError, jsonError.JSONDecodeError):
        return(context.bot.send_message(update.effective_message.chat.id, "File tidak dapat dibaca"))
    full = datetime.datetime.now().strftime("%Y/%m/%d")
    file_json = open("/home/{}/Documents/BoxDump.d/BoxDump.json".format(getpass.getuser()))
    baca = file_json.read()
    urai = json.loads(baca)
    cari = re.findall(r"\d{14}", baca)
    hitung = len(cari)
    if int(hitung) >= 10:
        filedump = open("/home/{}/Documents/BoxDump.d/BoxDump.json".format(getpass.getuser()), "rb")
        update.message.reply_text("Dump terlalu banyak")
        context.bot.send_document(update.effective_message.chat.id, document=filedump)
    else:
        ambil = urai[re.search(r"\d+\/\d+\/\d+", baca).group()][int(hitung) - 1]
        pesan = "<b>{}</b>\n\n".format(full)
        pesan += "Timestamp : <code>{}</code>\n".format(ambil["Timestamp"])
        pesan += "Status : {}\n".format(ambil["Status"])
        pesan += "Tinggi : {} cm\n".format(ambil["Tinggi"])
        pesan += "Jam : {}\n".format(ambil["Jam"])
        update.message.reply_text(pesan, parse_mode="HTML")

#Fungsi untuk membersihkan data log
@typing
def clear(update = Update, context = CallbackContext):
    if int(update.effective_message.chat.id) == int(json_setup["chatid"]):
        update.message.reply_text("Membersihkan log ...")
        if os.path.exists("log/aqualog.log"):
            open("log/aqualog.log", "w")
            jawaban = "Log berhasil dibersihkan"
        else:
            jawaban = "File log tidak ditemukan"
        sleep(1)
        context.bot.send_message(update.effective_message.chat.id, jawaban)
    else:
        context.bot.send_message(update.effective_message.chat.id, "Kamu orang asing 😡\nGak boleh suruh-suruh 😤")

#Fungsi untuk mengetahui status "aquamain.py"
@typing
def aquamain(update = Update, context = CallbackContext):
    keyboard = [    #Penyederhanaan variabel untuk penggunaan inline_keyboard
        [
            InlineKeyboardButton("Mulai Ulang", callback_data="aquamain")   #Konfigurasi inline_keyboard dengan pesan "Mulai Ulang", dan callback_data "aquamain"
        ]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)
    if check_aquamain() == False:
        status = "Proses tidak ditemukan"
    else:
        status = "Proses ditemukan"
    pesan = "<code>///aquamain.py///</code>\n\nStatus : {}".format(status)
    update.message.reply_text(pesan, parse_mode="HTML", reply_markup=inline_markup) #Menggunakan markup inline_markup

#Fungsi untuk melakukan mulai ulang pada telegrambot
@typing
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

#Fungsi untuk melakukan konfigurasi database server lokal
@typing
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

#Fungsi untuk mengirimkan log
@typing
def log(update = Update, context = CallbackContext):
    if os.path.exists("log/aqualog.log"):
        with open("log/aqualog.log") as data:
            panjang = len(data.read())
        if int(panjang) >= 2000:
            logfile = open("log/aqualog.log", "rb")
            update.message.reply_text("Log terlalu panjang")
            context.bot.send_document(update.effective_message.chat.id, document=logfile)
        elif int(panjang) <= 0:
            update.message.reply_text("Log kosong")
        else:
           update.message.reply_text(text=open("log/aqualog.log").read())
    else:
        update.message.reply_text("Log tidak ditemukan")

#Fungsi untuk mengirimkan log dalam bentuk file
@upload
def getlog(update = Update, context = CallbackContext):
    if os.path.exists("log/aqualog.log"):
        logfile = open("log/aqualog.log", "rb")
        context.bot.send_document(update.effective_message.chat.id, document=logfile)
    else:
        update.message.reply_text("Log tidak ditemukan")

#Fungsi untuk menampilkan status "aquastart.py"
@typing
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

#Fungsi untuk mengirimkan notifikasi
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
        Aqua.sendMessage(json_setup["chatid"], pesan[int(random.randint(0, len(pesan)))], parse_mode="HTML")

#Fungsi untuk mengirimkan pesan "ready" kepada pengguna apabila bot telah siap
def ready():
    Aqua = telegram.Bot(json_setup["token"])
    Aqua.sendMessage(json_setup["chatid"], "Aqua Ready")

#Fungsi untuk mengirimkan notifikasi peringatan/bahaya kepada pengguna
def alert():
    Aqua = telegram.Bot(json_setup["token"])
    pesan = [
        "Wiwuu Wiwuu Wiwuu, Aqua Mendeteksi kemungkinan Banjir",
        "Bahayaaa, Mohon Segera Cek TKP-nya Kakak !!!",
        "Ayo Segera Cek Kakak"
    ]
    Aqua.sendMessage(json_setup["chatid"], pesan[int(random.randint(0, len(pesan)))])

#Fungsi untuk mengirimkan notifikasi bahwa tombol telah ditekan
def pressed():
    Aqua = telegram.Bot(json_setup["token"])
    pesan = [
        "Tombol sudah ditekaaaan terimakasih",
        "Notifikasi telah dimatikan kakak",
        "Terimakasih atas bantuannya XD"
    ]
    Aqua.sendMessage(json_setup["chatid"], pesan[int(random.randint(0, len(pesan)))])

#Fungsi untuk cek status "aquastart.py"
def check():
    for process in psutil.process_iter():
        if process.cmdline() == ['python3', 'aquastart.py']:    #Jika proses ditemukan maka lakukan perintah dibawah
            return(True)    #Kembalikan value menjadi True
    return(False)   #Apabila proses tidak ditemukan maka kembalikan value menjadi valse

#Fungsi untuk cek status "aquamain.py"
def check_aquamain():
    get_pid = os.popen("ps ax | grep aquamain.py | grep -v grep").read()    #Ambil proses "aquamain.py"
    try:    #Coba jalankan perintah dibawah
        pid = re.search(r"\d+", get_pid).group()    #Cari Process ID "aquamain.py" menggunakan pola regex
    except: #Kecuali jika ..., jalankan perintah dibawah
        return(False)   #Apabila tidak ditemukan maka kembalikan value menjadi False
    return(pid) #Apabila PID ditemukan maka kembalikan value menjadi pid

#Fungsi untuk menangani callback data
@typing
def button(update: Update , context: CallbackContext) -> None:
    stranger = [
        "Kamu siapa ?",
        "Aqua gak kenal kamu",
        "Gak ah, baru kenal udah nyuruh-nyuruh",
        "Gak mau 😛",
        "Bayar dulu dong 😏",
        "Umm, enggak deh.\nAqua takut",
        "Entar aja yaa, kalo kita udah lama kenal 😋"
    ]
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
        if int(update.effective_message.chat.id) == int(json_setup["chatid"]):
            query.edit_message_text("Rebooting bot ...")
            a = os.popen("ps ax | grep aquabot.py | grep -v grep").read()
            try:
                os.kill(int(re.search(r"\d+", a).group()), signal.SIGKILL)
            except:
                pesan = "Bot gagal dimulai ulang"
                context.bot.send_message(update.effective_message.chat.id, pesan)
        else:
            query.edit_message_text(stranger[int(random.randint(0, len(stranger)))])

    elif query.data == "tentu":
        if int(update.effective_message.chat.id) == int(json_setup["chatid"]):
            query.edit_message_text("Menghentikan Script ...")
            a = os.popen("ps ax | grep aquastart.py | grep -v grep").read()
            if check() == True:
                try:
                    os.system("kill {}".format(re.search(r"\d+", a).group()))
                except:
                    context.bot.send_message(update.effective_message.chat.id, "Gagal Menghentikan Script")
                context.bot.send_message(update.effective_message.chat.id, "Script Berhasil Dihentikan")
            else:
                context.bot.send_message(update.effective_message.chat.id, "Script Sudah Berhenti.")
        else:
            query.edit_message_text(stranger[int(random.randint(0, len(stranger)))])

    elif query.data == "iya":
        if int(update.effective_message.chat.id) == int(json_setup["chatid"]):
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
        else:
            query.edit_message_text(stranger[int(random.randint(0, len(stranger)))])

    elif query.data == "100":
        if int(update.effective_message.chat.id) == int(json_setup["chatid"]):
            if os.path.exists("aquasetup.py"):
                try:
                    os.system("lxterminal -e python3 aquasetup.py")
                    sleep(1)
                finally:
                    query.edit_message_text("Script berhasil dijalankan\nMohon cek log untuk detail lebih lanjut.")
            else:
                query.edit_message_text("File tidak ditemukan !!!")
        else:
            query.edit_message_text(stranger[int(random.randint(0, len(stranger)))])

    elif query.data == "aquamain":
        if int(update.effective_message.chat.id) == int(json_setup["chatid"]):
            if os.path.exists("aquamain.py"):
                if check_aquamain() == False:
                    try:
                        os.system("lxterminal -e python3 aquamain.py")
                        sleep(1)
                    except:
                        query.edit_message_text("Gagal memulai ulang")
                    query.edit_message_text("Berhasil memulai ulang")
                else:
                    os.system("kill {}".format(int(check_aquamain())))
                    sleep(1)
                    os.system("lxterminal -e python3 aquamain.py")
                    if check_aquamain() == False:
                        query.edit_message_text("Gagal memulai ulang")
                    else:
                        query.edit_message_text("aquamain sudah berjalan")
            else:
                query.edit_message_text("File tidak ditemukan")
        else:
            query.edit_message_text(stranger[int(random.randint(0, len(stranger)))])

    else:
        pesan = [
            "Dasar",
            "Plin-plan",
            "Nyusahin aja",
            "Sabar, gaboleh ngatain 😊"
        ]
        query.edit_message_text(pesan[int(random.randint(0, len(pesan)))])

#Fungsi untuk melakukan perhitungan menit 
def minute_count():
    a = datetime.datetime.now().strftime("%M")  #Peyerhanaan variabel a dengan isi a adalah menit sekarang
    a = int(a) + 15 #a ditambah 15
    if a >= 60: #Jika a lebih dari sama dengan 60, maka
        a -= 60 #a dikurangi 60
    return(a)   #Kembalikan value menjadi a

#Konfigurasi handler untuk menangani perintah dan callback yang diterima
text_handler = MessageHandler(Filters.text, text)
dispatcher.add_handler(CommandHandler("setup", setup))
dispatcher.add_handler(CommandHandler("aquamain", aquamain))
dispatcher.add_handler(CommandHandler("clear", clear))
dispatcher.add_handler(CommandHandler("getlog", getlog))
dispatcher.add_handler(CommandHandler("log", log))
dispatcher.add_handler(CommandHandler("full", full))
dispatcher.add_handler(CommandHandler("last", last))
dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(CommandHandler("reboot", reboot))
command_handler = MessageHandler(Filters.command, command)
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(command_handler)
dispatcher.add_handler(text_handler)

#Jika perintah ini dijalankan secara langsung (bukan dari import), maka 
if __name__ == "__main__":
    try:    #Coba jalankan perintah ini
        updater.start_polling() #Memulai polling pada api telegrambot
    except: #Kecuali jika..., jalankan perintah dibawah
        logging.warning('This will get logged to a file')   #Semua log akan disimpan kedalam file
    finally:    #Akhirnya jalankan perintah dibawah
        ready() #Jalankan fungsi ready
        print("#########################")
        print("")
        print("   Aqua Telegram Bot")
        print(" dont close this window")
        print("")
        print("#########################")
        updater.idle()  #Rubah mode telegrambot menjadi idle