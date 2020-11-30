import RPi.GPIO as GPIO
import datetime, os, json, getpass, re, logging
from time import sleep
from urllib import request

logging.basicConfig(filename='log/aqualog.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

#Konfigurasi pin GPIO raspberry pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3, GPIO.OUT)  #LED Merah
GPIO.setup(5, GPIO.OUT)  #LED Hijau
GPIO.setup(7, GPIO.OUT)  #LED Biru
GPIO.setup(8, GPIO.IN)   #Sensor Siaga I
GPIO.setup(10, GPIO.IN)  #Sensor Siaga II
GPIO.setup(12, GPIO.IN)  #Sensor Siaga III
GPIO.setup(16, GPIO.IN) #Sensor Siaga IV
GPIO.input(18, GPIO.IN) #Sensor Bahaya
GPIO.input(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Tombol

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
    file = "/home/{}/Documents/BoxDump.d/BoxDump.json".format(nama)
    if os.path.exists(file) == False:
        with open(file, "w") as outfile:
            outfile.write(json_object)
    else:
        try:
            with open(file) as baca:
                a = baca.read()
                re.search(r"\d+\/\d+\/" + str(tgl), a).group()  #Lakukan pencarian dengan pola regex
        except: #Jika file tidak ditemukan, gagal dibuka, atau pencarian pola regex gagal, maka
            os.system("rm -rf {}".format(file)) #Hapus file

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
            status = str("Siaga I|II")
    elif (GPIO.input(10) == False):
        status = str("Siaga II")
        if (GPIO.input(12) == False):
            status = str("Siaga II|III")
    elif (GPIO.input(12) == False):
        status = str("Siaga III")
        if (GPIO.input(16) == False):
            status = str("Siaga III|IV")
    elif (GPIO.input(16) == False):
        status = str("Siaga IV")
        if (GPIO.input(18) == False):
            status = str("Siaga IV|Bahaya")
    elif (GPIO.input(18) == False):
        status = str("Bahaya")
    return(status)

#Fungsi untuk menentukan ketinggian air
def tinggi():
    tinggi = str()
    if (GPIO.input(8) == False):
        tinggi = str(json_setup["SI"])
        if (GPIO.input(10) == False):
            tinggi = str(json_setup["SI|II"])
    elif (GPIO.input(10) == False):
        tinggi = str(json_setup["SII"])
        if (GPIO.input(12) == False):
            tinggi = str(json_setup["SII|SIII"])
    elif (GPIO.input(12) == False):
        tinggi = str(json_setup["SIII"])
        if (GPIO.input(16) == False):
            tinggi = str(json_setup["SIII|IV"])
    elif (GPIO.input(16) == False):
        tinggi = str(json_setup["SIV"])
        if (GPIO.input(18) == False):
            tinggi = str(json_setup["SIV|B"])
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
    request.urlopen("http://10.30.1.247/proses.php?Timestamp={}&Tanggal={}&Waktu={}&Ketinggian={}+cm&Status={}".format(timestamp, tt, wk, tg, st))
    print("Data telah terkirim ke database")
    sleep(1)

def bundle():
    notif(str_status)
    insert_db(timestamp, str_status, str_tinggi, jam)
    insert_server(timestamp, full, jam, str_tinggi, str_status)
    with open("/home/{}/Documents/BoxDump.d/BoxDump.json".format(nama)) as json_file:
        data = json.load(json_file)
        temp = data["{}".format(full)]
        temp.append(report)
    write_json(data)

s1 = int()
s2 = int()
s3 = int()
s4 = int()
s5 = int()

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
            netral()
            if (GPIO.input(8) == False):
                if (GPIO.input(10) == False):
                    s2 += 1
                    if s2 == 20:
                        bundle()
                        s2 = 0
                s1 += 1
                if s1 == 20:
                    bundle()
                    s1 = 0
            elif (GPIO.input(10) == False):
                if (GPIO.input(12) == False):
                    s3 += 1
                    if s3 == 10:
                        bundle()
                        s3 = 0
                s2 += 1
                if s2 == 20:
                    bundle()
                    s2 = 0
            elif (GPIO.input(16) == False):
                if (GPIO.input(18) == False):
                    s5 += 1
                    if s5 == 5:
                        bundle()
                        s5 = 0
                s4 += 1
                if s4 == 10:
                    bundle()
                    s4 = 0
            elif (GPIO.input(18) == False):
                if (GPIO.input(16) == True):
                    bundle()
                    while (GPIO.input(22) == False):
                        netral()
                        sleep(1)
                        merah()
                        sleep(1)
                        alert()
                        sleep(1)
                        if (GPIO.input(22) == True):
                            print("Tombol telah ditekan")
                            pressed()
                            break
                    s5 = 0
            if (re.compile(r"00:00:0\d").search(jam)):
                for ulang in range(2):
                    cek()
                s1 = 0
                s2 = 0
                s3 = 0
                s4 = 0
                s5 = 0

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
            print("Siaga III : {}".format(s3))
            print("Siaga IV : {}".format(s4))
            print("Bahaya : {}".format(s5))
            sync_db(nama)
        except:
            logging.warning("This will get logged to a file")
        finally:
            sleep(1)
            os.system("clear")