import RPi.GPIO as GPIO
import datetime, os, json, getpass, re, logging
from time import sleep
from urllib import request

logging.basicConfig(filename='log/aqualog.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.OUT)  #LED Merah
GPIO.setup(5,GPIO.OUT)  #LED Hijau
GPIO.setup(7,GPIO.OUT)  #LED Biru
GPIO.setup(8,GPIO.IN)   #Sensor Siaga I
GPIO.setup(10,GPIO.IN)  #Sensor Siaga II
GPIO.setup(12,GPIO.IN)  #Sensor Bahaya
GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #Tombol

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
    "{}".format(datetime.datetime.now().strftime("%Y/%m/%d")) : [
        {
            "Timestamp" : datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            "Status" : "Mulai",
            "Tinggi" : "0M",
            "Jam" : datetime.datetime.now().strftime("%H:%M:%S")
        }
    ]
}

json_setup = json.loads(open("setup.json").read())
json_object = json.dumps(tmprpt, indent = 4)
nama = getpass.getuser()

def cek():
    thn = datetime.datetime.now().strftime("%Y-%m")
    tgl = datetime.datetime.now().strftime("%d")
    os.makedirs("/home/{}/Documents/BoxDump.d/{}".format(nama, thn), exist_ok=True)
    file = "/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)
    if os.path.exists(file) == False:
        with open(file, "w") as outfile:
            outfile.write(json_object)
    else:
        try:
            with open(file) as baca:
                a = baca.read()
                re.search(r"\d+\/\d+\/" + str(tgl), a).group()
        except:
            os.system("rm -rf {}".format(file))

for _ in range(2):
    cek()

def write_json(data, filename=("/home/{}/Documents/BoxDump.d/{}/{}.json".format(getpass.getuser(), datetime.datetime.now().strftime("%Y-%m"), datetime.datetime.now().strftime("%d")))):
    with open(filename, 'w') as jswrt:
        json.dump(data, jswrt, indent = 4)

def status():
    status = str()
    if (GPIO.input(8) == False):
        status = str("Siaga I")
        if (GPIO.input(10) == False):
            status = str("Siaga I/II")
    elif (GPIO.input(10) == False):
        status = str("Siaga II")
        if (GPIO.input(12) == False):
            status = str("Siaga II/Bahaya")
    elif (GPIO.input(12) == False):
        status = str("Bahaya")
    return(status)

def tinggi():
    tinggi = str()
    if (GPIO.input(8) == False):
        tinggi = str(json_setup["SI"])
        if (GPIO.input(10) == False):
            tinggi = str(json_setup["SI/II"])
    elif (GPIO.input(10) == False):
        tinggi = str(json_setup["SII"])
        if (GPIO.input(12) == False):
            tinggi = str(json_setup["SII/B"])
    elif (GPIO.input(12) == False):
        tinggi = str(json_setup["B"])
    return(tinggi)


def insert_server(timestamp, tanggal, waktu, ketinggian, status):
    tt = re.sub(r"[/]", "-", tanggal)
    wk = re.sub(r"[:]", "%3A", waktu)
    sT = re.sub(r"[ ]", "+", status)
    st = re.sub(r"[/]", "%2F", sT)
    tg = re.sub(r"[/]", "%2F", ketinggian)
    request.urlopen("http://10.30.1.247/proses.php?Timestamp={}&Tanggal={}&Waktu={}&Ketinggian={}+M&Status={}".format(timestamp, tt, wk, tg, st))
    print("Data telah terkirim ke database")
    sleep(1)

s1 = int()
s2 = int()
s3 = int()

if __name__ == "__main__":
    from aquabot import notif, alert, pressed
    from aquasetup import insert_db, validate_db, sync_db
    while True:
        thn = datetime.datetime.now().strftime("%Y-%m")
        tgl = datetime.datetime.now().strftime("%d")
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
                    if s2 == 10:
                        notif(str_status)
                        insert_db(timestamp, str_status, str_tinggi, jam)
                        insert_server(timestamp, full, jam, str_tinggi, str_status)
                        with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
                            data = json.load(json_file)
                            temp = data["{}".format(full)]
                            temp.append(report)
                        write_json(data)
                        s2 = 0
                s1 += 1
                if s1 == 20:
                    notif(str_status)
                    insert_db(timestamp, str_status, str_tinggi, jam)
                    insert_server(timestamp, full, jam, str_tinggi, str_status)
                    with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
                        data = json.load(json_file)
                        temp = data["{}".format(full)]
                        temp.append(report)
                    write_json(data)
                    s1 = 0
            elif (GPIO.input(10) == False):
                if (GPIO.input(12) == False):
                    s3 += 1
                    if s3 == 5:
                        notif(str_status)
                        insert_db(timestamp, str_status, str_tinggi, jam)
                        insert_server(timestamp, full, jam, str_tinggi, str_status)
                        with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
                            data = json.load(json_file)
                            temp = data["{}".format(full)]
                            temp.append(report)
                        write_json(data)
                        s3 = 0
                s2 += 1
                if s2 == 10:
                    notif(str_status)
                    insert_db(timestamp, str_status, str_tinggi, jam)
                    insert_server(timestamp, full, jam, str_tinggi, str_status)
                    with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
                        data = json.load(json_file)
                        temp = data["{}".format(full)]
                        temp.append(report)
                    write_json(data)
                    s2 = 0
            elif (GPIO.input(12) == False):
                if (GPIO.input(10) == True):
                    notif(str_status)
                    insert_db(timestamp, str_status, str_tinggi, jam)
                    insert_server(timestamp, full, jam, str_tinggi, str_status)
                    with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
                        data = json.load(json_file)
                        temp = data["{}".format(full)]
                        temp.append(report)
                    write_json(data)
                    s2 = 0
                    while (GPIO.input(16) == False):
                        netral()
                        sleep(1)
                        merah()
                        sleep(1)
                        alert()
                        sleep(1)
                        if (GPIO.input(16) == True):
                            print("Tombol telah ditekan")
                            pressed()
                            break

            if (re.compile(r"00:00:0\d").search(jam)):
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
            sync_db(nama, thn, tgl)
        except:
            logging.warning("This will get logged to a file")
        finally:
            sleep(1)
            os.system("clear")