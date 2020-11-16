import telepot
import time
import os
import json
import getpass
import re
import math
import random

tgl = time.strftime("%d %b", time.localtime())
bln = time.strftime("%b %Y", time.localtime())
thn = time.strftime("%Y", time.localtime())
jam = time.strftime("%H:%M", time.localtime())
full = time.strftime("%d %b %Y", time.localtime())
saat = str()

nama = getpass.getuser()

aquaBot = telepot.Bot("1480116644:AAHAWxJ0nv7AhcOr6O_OjFpNedly3lqDxd4")
aquaBot.getMe()

file_json = open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln))
data = json.loads(file_json.read())

def helper_count():
    if os.path.exists("Helper.json") == False:
        helper = {
            "Helper" : int(0)
        }
        json_helper = json.dumps(helper, indent = 4)
        with open("Helper.json", "w") as outfile:
            outfile.write(json_helper)
    else:
        file_helper = open("Helper.json")
        data_helper = json.loads(file_helper.read())
        for key, value in data_helper.items():
            value += 1
            helper = {
                "Helper" : value
            }
            json_helper = json.dumps(helper, indent = 4)
            with open("Helper.json", "w") as outfile:
                json.dump(helper, outfile)
        print("Jumlah Helper : {}".format(value))
        


def tlgrm(msg):
    chat_id = msg["chat"]["id"]
    chat_type = msg["chat"]["type"]
    command = msg["text"]
    
    file_helper = open("Helper.json")
    data_helper = json.loads(file_helper.read())

    print("Perintah diterima : {}".format(command))

    for key, value in data_helper.items():
        if (re.compile(r"/last").search(command)):
            aquaBot.sendMessage(chat_id, f"<b>Status Terakhir {'{}'.format(full)}</b> :\n\n{(json.dumps(data['{}'.format(tgl)][value], indent=4, sort_keys=False))}","HTML")
        elif (re.compile(r"/full").search(command)):
            aquaBot.sendMessage(chat_id, f"<b>Tanggal {'{}'.format(full)}</b> :\n\n{(json.dumps(data['{}'.format(tgl)], indent=4, sort_keys=False))}","HTML")

    if (re.compile(r"/aqua").search(command)):
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

#helper_count()
aquaBot.message_loop(tlgrm)
print("Masukkan Perintah : ")

while True:
    if (re.compile(r"0\d\:\d\d").search(jam)):
        saat = "Pagi"
    elif (re.compile(r"1[01234]\:\d\d").search(jam)):
        saat = "Siang"
    elif (re.compile(r"1[5678]\:\d\d").search(jam)):
        saat = "Sore"
    else:
        saat = "Malam"
    time.sleep(5)