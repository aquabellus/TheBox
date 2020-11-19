import RPi.GPIO as GPIO
import time, telepot, os, json, getpass, re, math, random, pandas, mysql.connector
from telepot.namedtuple import ReplyKeyboardMarkup
from aquasetup import json_setup, insert_db

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.OUT)  #LED Merah
GPIO.setup(5,GPIO.OUT)  #LED Hijau
GPIO.setup(7,GPIO.OUT)  #LED Biru
#GPIO.setup(11,GPIO.OUT) #LED VCC
GPIO.setup(8,GPIO.IN)   #Sensor Siaga I
GPIO.setup(10,GPIO.IN)  #Sensor Siaga II
GPIO.setup(12,GPIO.IN)  #Sensor Bahaya
GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #Tombol
#Pin 3.3V => Pin Button
def netral():
    GPIO.output(3,True)
    GPIO.output(5,True)
    GPIO.output(7,True)

def merah():
    GPIO.output(3,False)
    GPIO.output(5,True)
    GPIO.output(7,True)

def kuning():
    GPIO.output(3,False)
    GPIO.output(5,False)
    GPIO.output(7,True)

def hijau():
    GPIO.output(3,True)
    GPIO.output(5,False)
    GPIO.output(7,True)

tmprpt = {
    "{}".format(time.strftime("%Y/%m/%d", time.localtime())) : [
        {
            "Status" : "Mulai",
            "Jam" : time.strftime("%H:%M:%S", time.localtime())
        }
    ]
}

json_object = json.dumps(tmprpt, indent = 4)

def cek():
    nama = getpass.getuser()
    bln = time.strftime("%b %Y", time.localtime())
    thn = time.strftime("%Y", time.localtime())
    if os.path.exists("/home/{}/Documents/BoxDump.d".format(nama)) == False:
        os.makedirs("/home/{}/Documents/BoxDump.d/{}".format(nama,thn))
        with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln), "w") as outfile:
            outfile.write(json_object)
    else:
        if os.path.exists("/home/{}/Documents/BoxDump.d/{}".format(nama,thn)) == False:
            os.makedirs("/home/{}/Documents/BoxDump.d/{}".format(nama,thn))
            with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln), "w") as outfile:
                outfile.write(json_object)
        else:
            if os.path.exists("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln)) == False:
                with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln), "w") as outfile:
                    outfile.write(json_object)

cek()

def write_json(data, filename=("/home/{}/Documents/BoxDump.d/{}/{}.json".format(getpass.getuser(), time.strftime("%Y", time.localtime()), time.strftime("%b %Y", time.localtime())))):
    with open(filename, 'w') as jswrt:
        json.dump(data, jswrt, indent = 4)

aquaBot = telepot.Bot(json_setup["token"])
telecheck = aquaBot.getMe()

file_json = open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(getpass.getuser(), time.strftime("%Y", time.localtime()), time.strftime("%b %Y", time.localtime())))
data = json.loads(file_json.read())

def greet():
    jam = time.strftime("%H:%M:%S", time.localtime())
    if (re.compile(r"0\d\:\d\d").search(jam)):
        return("Pagi")
    elif (re.compile(r"1[01234]\:\d\d").search(jam)):
        return("Siang")
    elif (re.compile(r"1[5678]\:\d\d").search(jam)):
        return("Sore")
    else:
        return("Malam")

def tlgrm(msg):
    full = time.strftime("%Y/%m/%d", time.localtime())
    chat_id = msg["chat"]["id"]
    chat_type = msg["chat"]["type"]
    command = msg["text"]
    username = msg["from"]["username"]
    
    print("Perintah diterima : {}".format(command))

    if (re.compile(r"/start").search(command)):
        keyboard = ReplyKeyboardMarkup(keyboard=[["/aqua"]],resize_keyboard=True, one_time_keyboard=True)
        pesan = "Halo, namaku Aqua\nAku adalah bot yang akan membantumu untuk mengontrol alat-alat yang dibuat oleh aquabellus."
        pesan += "\nKalo ingin memanggilku, pencet tombol yang disediakan yaa"
        aquaBot.sendMessage(chat_id, pesan, "HTML", reply_markup=keyboard)

    elif (re.compile(r"/last").search(command)):
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

    elif (re.compile(r"/about").search(command)):
        pesan = "Aqua adalah bot yang dibuat untuk membantu pengguna dalam menggunakan produk-produk aquabellus\n"
        pesan += "Untuk keterangan lebih lanjut, silahkan menuju ke tautan berikut.\n"
        pesan += "<a href='https://github.com/aquabellus'>Github</a>"
        aquaBot.sendMessage(chat_id, pesan, "HTML")

    elif (re.compile(r"/id").search(command)):
        if chat_type == "private":
            aquaBot.sendMessage(chat_id, "Hai {}\nSelamat {}\nChat ID kamu adalah : <code>{}</code>".format(username, greet(), chat_id),"HTML")
        elif chat_type == "supergroup":
            aquaBot.sendMessage(chat_id, "Hai {}\nSelamat {}\nChat ID kamu adalah : <code>{}</code>\nChat ID grup ini adalah : <code>{}</code>".format(username, greet(), msg["from"]["id"],chat_id),"HTML")
        else :
            aquaBot.sendMessage(chat_id, "Hai {}\nSelamat {}\nChat ID {} ini adalah : <code>{}</code>".format(username, greet(), chat_type, chat_id),"HTML")

def notif(status,jam):
    aquaBot.sendMessage(json.loads(open("setup.json").read())['chatid'],"Status {} Pada Pukul {}".format(status,jam))

def pressed():
    pesan = [
        "Tombol sudah ditekaaaan terimakasih",
        "Notifikasi telah dimatikan kakak",
        "Terimakasih atas bantuannya XD"
    ]
    aquaBot.sendMessage(json.loads(open("setup.json").read())['chatid'], pesan[random.randrange(len(pesan))], "HTML")

def alert():
    pesan = [
        "Bahaya bahayaaaa Aqua mendeteksi kemungkinan banjir",
        "Wi Wu Wi Wu Wi Wuuuuuu",
        "Sudah terdeteksi bahayaaa\nAyo cek dan di tekan tombolnya"
    ]
    aquaBot.sendMessage(json.loads(open("setup.json").read())['chatid'], pesan[random.randrange(len(pesan))], "HTML")

aquaBot.message_loop(tlgrm)
print(telecheck)
print("Masukkan Perintah : ")

s1 = int()
s2 = int()

if __name__ == "__main__":
    while True:
        bln = time.strftime("%b %Y", time.localtime())
        thn = time.strftime("%Y", time.localtime())
        jam = time.strftime("%H:%M:%S", time.localtime())
        full = time.strftime("%Y/%m/%d", time.localtime())
        nama = getpass.getuser()
        greet()
        cek()
        netral()
        if (GPIO.input(8) == False):
            s1 += 1
            if s1 >= 20:
                s1 = 0
                notif("Siaga I",jam)
                insert_db("Siaga I")
                with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln)) as json_file:
                    data = json.load(json_file)
                    wrjsn = data["{}".format(full)]        
                    s1rpt = {
                        "Status" : "Siaga I",
                        "Jam" : jam
                    }
                    wrjsn.append(s1rpt)
                write_json(data)
            else:
                print(("Status Siaga I Telah Terekam Sebanyak {} Kali").format(s1))
        elif (GPIO.input(10) == False):
            s2 += 1
            if s2 >= 10:
                s2 = 0
                notif("Siaga II",jam)
                insert_db("Siaga II")
                with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln)) as json_file:
                    data = json.load(json_file)
                    wrjsn = data["{}".format(full)]        
                    s2rpt = {
                        "Status" : "Siaga II",
                        "Jam" : jam
                    }
                    wrjsn.append(s2rpt)
                write_json(data)
            else:
                print(("Status Siaga II Telah Terekam Sebanyak {} Kali").format(s2))
        elif (GPIO.input(12) == False):
            notif("Bahaya",jam)
            insert_db("Bahaya")
            with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln)) as json_file:
                data = json.load(json_file)
                wrjsn = data["{}".format(full)]        
                bhya = {
                    "Status" : "Bahaya",
                    "Jam" : jam
                }
                wrjsn.append(bhya)
            write_json(data)
            while True:
                if (GPIO.input(16) == False):
                    merah()
                    time.sleep(0.5)
                    netral()
                    time.sleep(0.5)
                    alert()
                    time.sleep(1)
                else:
                    print("Tombol Telah Ditekan")
                    pressed()
                    break
        else:
            print("Status Aman")

        convert = pandas.DataFrame(data['{}'.format(full)])
        time.sleep(1)