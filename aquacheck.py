import telegram, json, mysql.connector, re, time

#Variabel template
template = {
    "host" : "YOUR HOST",
    "user" : "YOUR USER",
    "passwd" : "YOUR PASSWORD",
    "database" : "YOUR DATABASE",
    "token" : "YOUR TOKEN",
    "chatid" : "YOUR CHAT ID",
    "SI" : "FIRST HEIGHT",
    "SI/II" : "FIRST/SECOND HEIGHT",
    "SII" : "SECOND HEIGHT",
    "SII/B" : "SECOND/DANGER HEIGHT",
    "B" : "DANGER HEIGHT"
}

ambil = json.dumps(template, indent=4)

#Fungsi untuk melakukan cek validasi pada file .json
def check_json():
    try:
        json.loads(open("./setup.json").read()) #Buka file .json dengan atribut read
    except(FileNotFoundError):  #Kecuali jika file tidak ditemukan, maka
        open("./setup.json", "w").write(ambil)  #Tulis ulang file .json dengan template
        return("File not found")    #Kembalikan value menjadi file not found
    except: #Kecuali jika ..., maka
        return("Error") #Kembalikan value menjadi Error
    return("OK")    #Apabila berhasil, kembalikan value menjadi OK

#Fungsi untuk melakukan cek pada layanan dan konfigurasi bot
def check_bot():
    try:
        checkBot = telegram.Bot(baca["token"])
        checkBot.sendMessage(baca["chatid"], "Bot Check Is Passed")
    except:
        if re.search(r"YOUR\s\w+", baca["token"]):  #Jika ditemukan string "YOUR xxxx" dengan xxxx adalah huruf, maka
            return("Field is not configured")
        else:
            return("Error")
    return("OK")

#Fungsi untuk melakukan koneksi dengan database
def check_database():
    try:
        db = mysql.connector.connect( host=baca["host"], user=baca["user"], passwd=baca["passwd"], auth_plugin=baca["auth"] )
        db.is_connected()
    except:
        if re.search(r"YOUR\s\w+", baca["host"]):
            return("Field is not configured")
        else:
            return("Error")
    return("OK")

a = 10

print("##########################")
print("#                        #")
print("#  Aqua Service Checker  #")
print("#                        #")
print("##########################")
print("")
print("JSON Status : {}".format(check_json()))
print("")
print("")
baca = json.loads(open("./setup.json").read())
print("Bot Status : {}".format(check_bot()))
print("Database Status : {}".format(check_database()))
print("")
while a:    #Lakukan perulangan dengan jumlah a
    a -= 1  #Kurangi a dengan 1
    print(f"Pesan ini akan hilang dalam {a}", end="\r")
    time.sleep(1)   #Jeda waktu selama 1 detik
