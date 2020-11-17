from aquarefile import time, telepot, os, json, getpass, re, math, random, pandas
from aquarefile import nama, jam, tgl, thn, bln, full
saat = str()

aquaBot = telepot.Bot("1480116644:AAHAWxJ0nv7AhcOr6O_OjFpNedly3lqDxd4")
aquaBot.getMe()

file_json = open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln))
data = json.loads(file_json.read())
convert = pandas.DataFrame(data['{}'.format(tgl)])

def greet():
    if (re.compile(r"0\d\:\d\d").search(jam)):
        saat = "Pagi"
    elif (re.compile(r"1[01234]\:\d\d").search(jam)):
        saat = "Siang"
    elif (re.compile(r"1[5678]\:\d\d").search(jam)):
        saat = "Sore"
    else:
        saat = "Malam"

def tlgrm(msg):
    chat_id = msg["chat"]["id"]
    chat_type = msg["chat"]["type"]
    command = msg["text"]
    
    print("Perintah diterima : {}".format(command))

    if (re.compile(r"/last").search(command)):
        aquaBot.sendMessage(chat_id, f"<b>Status Terakhir {'{}'.format(full)}</b> :\n\n{(convert.tail(1))}","HTML")
    elif (re.compile(r"/full").search(command)):
        aquaBot.sendMessage(chat_id, f"<b>Tanggal {'{}'.format(full)}</b> :\n\n{(convert)}","HTML")

    elif (re.compile(r"/aqua").search(command)):
        pesan = [
            "Dalem ?",
            "Kenapa ?",
            "Hadir"
        ]
        aquaBot.sendMessage(chat_id, "{}".format(pesan[random.randrange(len(pesan))]))
    elif (re.compile(r"/id").search(command)):
        if chat_type == "private":
            aquaBot.sendMessage(chat_id, "Hai {}\nSelamat {}\nChat ID kamu adalah : <code>{}</code>".format(msg["chat"]["first_name"], saat, chat_id),"HTML")
        elif chat_type == "supergroup":
            aquaBot.sendMessage(chat_id, "Hai {}\nSelamat {}\nChat ID kamu adalah : <code>{}</code>\nChat ID grup ini adalah : <code>{}</code>".format(msg["from"]["first_name"], saat, msg["from"]["id"],chat_id),"HTML")
        else :
            aquaBot.sendMessage(chat_id, "Hai\nSelamat {}\nChat ID {} ini adalah : <code>{}</code>".format(saat, chat_type, chat_id),"HTML")

def notif(status,jam):
    aquaBot.sendMessage(732796378,"Status {} Pada Pukul {}".format(status,jam))

aquaBot.message_loop(tlgrm)
print("Masukkan Perintah : ")

while True:
        greet()
        # time.sleep(5)