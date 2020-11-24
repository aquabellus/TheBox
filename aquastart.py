import RPi.GPIO as GPIO
import datetime, os, json, getpass, re, math, random, pandas, logging
from aquabot import notif, alert, pressed
from aquasetup import json_setup, insert_db
from time import sleep
from urllib import request

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

json_object = json.dumps(tmprpt, indent = 4)
nama = getpass.getuser()
path = os.path.dirname(os.path.realpath(__file__))
pid = str(os.getpid())
pidfile = "{}/helper/aquastart.pid".format(path)

def cek():
    thn = datetime.datetime.now().strftime("%Y-%m")
    tgl = datetime.datetime.now().strftime("%d")
    if os.path.exists("/home/{}/Documents/BoxDump.d".format(nama)) == False:
        os.makedirs("/home/{}/Documents/BoxDump.d/{}".format(nama,thn))
        with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,tgl), "w") as outfile:
            outfile.write(json_object)
    else:
        if os.path.exists("/home/{}/Documents/BoxDump.d/{}".format(nama,thn)) == False:
            os.makedirs("/home/{}/Documents/BoxDump.d/{}".format(nama,thn))
            with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,tgl), "w") as outfile:
                outfile.write(json_object)
        else:
            if os.path.exists("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,tgl)) == False:
                with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,tgl), "w") as outfile:
                    outfile.write(json_object)

    file_json = open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl))
    data = json.loads(file_json.read())
    saring = re.sub("[^0-9/]", "", str(data))
    if (re.search(r"\d+\/\d+\/" + tgl, saring)):
        return("Correct")
    else:
        with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
            data = json.load(json_file)
            data.clear()
            data.update(tmprpt)
        with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
            json.dump(data, json_file, indent=4)
        return("Incorrect")


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

if os.path.exists("helper/") == False:
    os.mkdir("helper/")
if os.path.isfile(pidfile):
    print("{} Sudah Tersedia, Menulis Ulang ...".format(pidfile))
open(pidfile, 'w').write(pid)

def insert_server(timestamp, tanggal, waktu, ketinggian, status):
    tt = re.sub(r"[/]", "-", tanggal)
    wk = re.sub(r"[:]", "%3A", waktu)
    sT = re.sub(r"[ ]", "+", status)
    st = re.sub(r"[/]", "%2F", sT)
    request.urlopen("http://10.30.1.247/input_data_php/proses.php?timestamp={}&tanggal={}&waktu={}&ketinggian={}&status={}".format(timestamp, tt, wk, ketinggian, st))

s1 = int()
s2 = int()
s3 = int()

if __name__ == "__main__":
    logging.basicConfig(filename='log/aquastart.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    while True:
        thn = datetime.datetime.now().strftime("%Y-%m")
        tgl = datetime.datetime.now().strftime("%d")
        jam = datetime.datetime.now().strftime("%H:%M:%S")
        full = datetime.datetime.now().strftime("%Y/%m/%d")
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        report = {
            "Timestamp" : timestamp,
            "Status" : status(),
            "Tinggi" : tinggi(),
            "Jam" : jam
        }   

        try:
            cek()
        except:
            logging.warning('This will get logged to a file')
        finally:
            netral()
            if (GPIO.input(8) == False):
                if (GPIO.input(10) == False):
                    s2 += 1
                    if s2 == 10:
                        notif(status())
                        insert_db(timestamp, status(), tinggi())
                        insert_server(timestamp, full, jam, tinggi(), status())
                        with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
                            data = json.load(json_file)
                            temp = data["{}".format(full)]
                            temp.append(report)
                        write_json(data)
                        s2 = 0
                s1 += 1
                if s1 == 20:
                    notif(status())
                    insert_db(timestamp, status(), tinggi())
                    insert_server(timestamp, full, jam, tinggi(), status())
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
                        notif(status())
                        insert_db(timestamp, status(), tinggi())
                        insert_server(timestamp, full, jam, tinggi(), status())
                        with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
                            data = json.load(json_file)
                            temp = data["{}".format(full)]
                            temp.append(report)
                        write_json(data)
                        s3 = 0
                s2 += 1
                if s2 == 10:
                    notif(status())
                    insert_db(timestamp, status(), tinggi())
                    insert_server(timestamp, full, jam, tinggi(), status())
                    with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
                        data = json.load(json_file)
                        temp = data["{}".format(full)]
                        temp.append(report)
                    write_json(data)
                    s2 = 0
            elif (GPIO.input(12) == False):
                if (GPIO.input(10) == True):
                    notif(status())
                    insert_db(timestamp, status(), tinggi())
                    insert_server(timestamp, full, jam, tinggi(), status())
                    with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
                        data = json.load(json_file)
                        temp = data["{}".format(full)]
                        temp.append(report)
                    write_json(data)
                    s3 = 0
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

            print("##########")
            print("aquastart.py")
            print("")
            print("Status JSON : {}".format(cek()))
            print("Jumlah Deteksi Sensor")
            print("")
            print("Siaga I : {}x".format(s1))
            print("Siaga II : {}x".format(s2))
            print("Bahaya : {}x".format(s3))
            print("")
            print("")
            if (re.compile(r"00:00:\d\d").search(jam)):
                s1 = 0
                s2 = 0
                s3 = 0
        sleep(1)
        os.system("clear")