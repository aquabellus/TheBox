import RPi.GPIO as GPIO
import datetime, os, json, getpass, re, math, random, pandas, logging
from aquabot import notif, alert, pressed
from aquasetup import json_setup, insert_db
from time import sleep

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
            "Status" : "Mulai",
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

def siagaI(s1, s2_2):
    if (GPIO.input(8) == False):
        if (GPIO.input(10) == False):
            s2_2 += 1
            if s2_2 >= 20:
                notif(status())
                insert_db(status())
                with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl)) as json_file:
                    data = json.load(json_file)["{}".format(full)].append(report)
                write_json(data)
                s2_2 = 0
        s1 += 1
        if s1 >= 20:
            notif(status())
            insert_db(status())
            with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,tgl)) as json_file:
                data = json.load(json_file)["{}".format(full)].append(report)
            write_json(data)
            s1 = 0

def siagaII(s2, s3):
    if (GPIO.input(10) == False):
        if (GPIO.input(12) == False):
            s3 += 1
            if s3 >= 10:
                notif(status())
                insert_db(status())
                with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,tgl)) as json_file:
                    data = json.load(json_file)["{}".format(full)].append(report)
                write_json(data)
                s3 = 0
        s2 += 1
        if s2 >= 10:
            notif(status())
            insert_db(status())
            with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,tgl)) as json_file:
                data = json.load(json_file)["{}".format(full)].append(report)
            write_json(data)
            s2 = 0

def danger(s3):
    if (GPIO.input(12) == False):
        if (GPIO.input(10) == True):
            notif(status())
            insert_db(status())
            with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,tgl)) as json_file:
                data = json.load(json_file)["{}".format(full)].append(report)
            write_json(data)
            s3 = 0
            while True:
                if (GPIO.input(16) == False):
                    merah()
                    sleep(1)
                    netral()
                    sleep(1)
                    alert()
                    sleep(1)
                else:
                    print("Tombol Telah Ditekan")
                    pressed()
                    break

if os.path.exists("helper/") == False:
    os.mkdir("helper/")
if os.path.isfile(pidfile):
    print("{} Sudah Tersedia, Menulis Ulang ...".format(pidfile))
open(pidfile, 'w').write(pid)

logging.basicConfig(filename='log/aquastart.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == "__main__":
    s1 = int()
    s2 = int()
    s3 = int()
    s2_2 = int()
    while True:
        thn = datetime.datetime.now().strftime("%Y-%m")
        tgl = datetime.datetime.now().strftime("%d")
        jam = datetime.datetime.now().strftime("%H:%M:%S")
        full = datetime.datetime.now().strftime("%Y/%m/%d")
        report = {
            "Status" : status(),
            "Jam" : jam
        }   

        if (re.compile(r"00\:00\:\d\d").search(jam)):
            cek()
        try:
            netral()
            danger(s3)
            siagaII(s2, s3)
            siagaI(s1, s2_2)
        except(NameError, SystemError):
            logging.error('This will get logged to a file')
        except(SystemExit, KeyboardInterrupt):
            logging.warning('This will get logged to a file')
        finally:
            print("Status Siaga I, II, dan Bahaya Secara Berurutan Telah Terekam Sebanyak {}/{}/{} Kali".format(s1, s2, s3))
            if (re.compile(r"00:0[01]:\d\d").search(jam)):
                s1 = 0
                s2 = 0
                s3 = 0
                s2_2 = 0
        sleep(1)