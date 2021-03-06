import RPi.GPIO as GPIO
import datetime, os, json, getpass, re, logging
from time import sleep
from urllib import request

logging.basicConfig(filename='log/aqualog.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

#Konfigurasi pin GPIO raspberry pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3, GPIO.OUT)  #LED Merah
GPIO.setup(8, GPIO.IN)   #Sensor Siaga I
GPIO.setup(10, GPIO.IN)  #Sensor Siaga II
GPIO.setup(12, GPIO.IN)  #Sensor Siaga III
GPIO.setup(16, GPIO.IN) #Sensor Siaga IV
GPIO.setup(18, GPIO.IN) #Sensor Bahaya
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Tombol

#Template yang digunakan untuk menulis file .json
tmprpt = {
    "{}".format(datetime.datetime.now().strftime("%Y/%m/%d")) : [
        {
            "Timestamp" : datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            "Status" : "Mulai",
            "Tinggi" : "0 cm",
            "Jam" : datetime.datetime.now().strftime("%H:%M:%S")
        }
    ]
}

#Penyederhanaan variabel
json_setup = json.loads(open("setup.json").read())
json_object = json.dumps(tmprpt, indent = 4)
nama = getpass.getuser()

#Fungsi untuk melakukan cek file dump
def cek():
    tgl = datetime.datetime.now().strftime("%d")
    os.makedirs("/home/{}/Documents/BoxDump.d".format(nama), exist_ok=True)
    fileJson = "/home/{}/Documents/BoxDump.d/BoxDump.json".format(nama)
    if os.path.exists(fileJson) == False:
        with open(fileJson, "w") as outfile:
            outfile.write(json_object)
    else:
        try:
            with open(fileJson) as baca:
                a = baca.read()
                re.search(r"\d+\/\d+\/" + str(tgl), a).group()  #Lakukan pencarian dengan pola regex
        except: #Jika file tidak ditemukan, gagal dibuka, atau pencarian pola regex gagal, maka
            os.system("rm -rf {}".format(fileJson)) #Hapus file

for _ in range(2):  #Perulangan dengan hitungan 2
    cek()   #Panggil fungsi cek

#Fungsi untuk menulis data .json
def write_json(data, filename=("/home/{}/Documents/BoxDump.d/BoxDump.json".format(getpass.getuser()))):
    with open(filename, 'w') as jswrt:
        json.dump(data, jswrt, indent = 4)

#Fungsi untuk menentukan status keadaan air
def status():
    status = str()
    if (GPIO.input(8) == False):
        status = str("Siaga I")
        if (GPIO.input(10) == False):
            status = str("Siaga I")
    elif (GPIO.input(10) == False):
        status = str("Siaga I")
        if (GPIO.input(12) == False):
            status = str("Siaga II")
    elif (GPIO.input(12) == False):
        status = str("Siaga II")
        if (GPIO.input(16) == False):
            status = str("Siaga II")
    elif (GPIO.input(16) == False):
        status = str("Siaga II")
        if (GPIO.input(18) == False):
            status = str("Bahaya")
    elif (GPIO.input(18) == False):
        status = str("Bahaya")
    return(status)

#Fungsi untuk menentukan ketinggian air
def tinggi():
    tinggi = str()
    if (GPIO.input(8) == False):
        tinggi = str(json_setup["SI"])
        if (GPIO.input(10) == False):
            tinggi = str(json_setup["SI"])
    elif (GPIO.input(10) == False):
        tinggi = str(json_setup["SI"])
        if (GPIO.input(12) == False):
            tinggi = str(json_setup["SII"])
    elif (GPIO.input(12) == False):
        tinggi = str(json_setup["SII"])
        if (GPIO.input(16) == False):
            tinggi = str(json_setup["SII"])
    elif (GPIO.input(16) == False):
        tinggi = str(json_setup["SII"])
        if (GPIO.input(18) == False):
            tinggi = str(json_setup["B"])
    elif (GPIO.input(18) == False):
        tinggi = str(json_setup["B"])
    return(tinggi)

#Fungsi untuk melakukan koneksi dan menulis data pada server database pusat
def insert_server(timestamp, tanggal, waktu, ketinggian, status):
    tt = re.sub(r"[/]", "-", tanggal)
    wk = re.sub(r"[:]", "%3A", waktu)
    sT = re.sub(r"[ ]", "+", status)
    st = re.sub(r"[|]", "%7C", sT)
    tg = re.sub(r"[|]", "%7C", ketinggian)
    request.urlopen("http://aquabellus.pagekite.me/html/proses.php?Timestamp={}&Tanggal={}&Waktu={}&Ketinggian={}+cm&Status={}".format(timestamp, tt, wk, tg, st))
    print("Data telah terkirim ke database")
    sleep(1)

def bundle_2():
    notif(str_status)
    insert_db(timestamp, str_status, str_tinggi, jam)
    insert_server(timestamp, full, jam, str_tinggi, str_status)

def bundle_1():
    with open("/home/{}/Documents/BoxDump.d/BoxDump.json".format(nama)) as json_file:
        data = json.load(json_file)
        temp = data["{}".format(full)]
        temp.append(report)
    write_json(data)

def kirim():
    a = datetime.datetime.now().strftime("%S")
    a = int(a) + 5
    if a >= 60:
        a -= 60
    return(a)

s1 = int()
s2 = int()
s3 = int()
alrt = int()

if __name__ == "__main__":
    from aquabot import notif, alert, pressed
    from aquasetup import insert_db, sync_db
    while True:
        jam = datetime.datetime.now().strftime("%H:%M:%S")
        full = datetime.datetime.now().strftime("%Y/%m/%d")
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        str_tinggi = tinggi()
        str_status = status()
        report = {
            "Timestamp" : timestamp,
            "Status" : str_status,
            "Tinggi" : str_tinggi,
            "Jam" : jam
        }

        try:
            cek()
            GPIO.output(3, False)
            if (GPIO.input(8) == False):
                if (GPIO.input(10) == False):
                    s1 += 1
                    if s1 == 20:
                        bundle_1()
                        bundle_2()
                        s1 = 0
                s1 += 1
                if s1 == 20:
                    bundle_1()
                    bundle_2()
                    s1 = 0
            elif (GPIO.input(10) == False):
                if (GPIO.input(12) == False):
                    s2 += 1
                    if s2 == 10:
                        bundle_1()
                        bundle_2()
                        s2 = 0
                s1 += 1
                if s1 == 20:
                    bundle_1()
                    bundle_2()
                    s1 = 0
            elif (GPIO.input(16) == False):
                if (GPIO.input(18) == False):
                    bundle_1()
                    bundle_2()
                    GPIO.input(3, True)
                s2 += 1
                if s2 == 10:
                    bundle_1()
                    bundle_2()
                    s2 = 0
            elif (GPIO.input(18) == False):
                if (GPIO.input(16) == True):
                    bundle_1()
                    bundle_2()
                    alert()
                    alrt = kirim()
                    while (GPIO.input(22) == False):
                        GPIO.output(3, True)
                        sleep(0.25)
                        GPIO.output(3, False)
                        sleep(0.25)
                        if int(datetime.datetime.now().strftime("%S")) == int(alrt):
                            alert()
                            alrt = kirim()
                        if (GPIO.input(22) == True):
                            pressed()
                            print("Tombol telah ditekan")
                            break

            if (re.compile(r"00:00:0\d").search(jam)):
                for ulang in range(2):
                    cek()
                s1 = 0
                s2 = 0
                s3 = 0

            print("#########################")
            print("")
            print("   Monitoring Script")
            print(" dont close this window")
            print("")
            print("#########################")
            print("\n"*1)
            print("Hasil :")
            print("Siaga I : {}".format(s1))
            print("Siaga II : {}".format(s2))
            print("Bahaya : {}".format(s3))
            sync_db(nama)
        except:
            logging.warning("This will get logged to a file")
        finally:
            sleep(1)
            os.system("clear")