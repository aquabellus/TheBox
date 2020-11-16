import RPi.GPIO as GPIO
import time
import json
import os
import getpass
from Scripts.aquanotif import notif,helper_count

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

tgl = time.strftime("%d %b", time.localtime())
bln = time.strftime("%b %Y", time.localtime())
thn = time.strftime("%Y", time.localtime())
jam = time.strftime("%H:%M", time.localtime())

nama = getpass.getuser()

s1 = int()
s2 = int()

def write_json(data, filename=("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln))):
    with open(filename, 'w') as jswrt:
        json.dump(data, jswrt, indent = 4)

tmprpt = {
    "{}".format(tgl) : [
        {
            "Status" : "Mulai",
            "Jam" : jam
        }
    ]
}

json_object = json.dumps(tmprpt, indent = 4)

while True:
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
    netral()
    if (GPIO.input(8) == False):
        s1 += 1
        if s1 >= 20:
            s1 = 0
            helper_count()
            notif("Siaga I",jam)
            with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln)) as json_file:
                data = json.load(json_file)
                wrjsn = data["{}".format(tgl)]        
                s1rpt = {
                    "Status" : "Siaga I",
                    "Jam" : jam
                }
                wrjsn.append(s1rpt)
            write_json(data)
            while True:
                if (GPIO.input(16) == False):
                    hijau()
                    time.sleep(2)
                    netral()
                    time.sleep(2)
                else:
                    print("Tombol Telah Ditekan")
                    break
        else:
            print(("Status Siaga I Telah Terekam Sebanyak {} Kali").format(s1))
    elif (GPIO.input(10) == False):
        s2 += 1
        if s2 >= 10:
            s2 = 0
            helper_count()
            notif("Siaga II",jam)
            with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln)) as json_file:
                data = json.load(json_file)
                wrjsn = data["{}".format(tgl)]        
                s2rpt = {
                    "Status" : "Siaga II",
                    "Jam" : jam
                }
                wrjsn.append(s2rpt)
            write_json(data)
            while True:
                if (GPIO.input(16) == False):
                    kuning()
                    time.sleep(1)
                    netral()
                    time.sleep(1)
                else:
                    print("Tombol Telah Ditekan")
                    break
        else:
            print(("Status Siaga II Telah Terekam Sebanyak {} Kali").format(s2))
    elif (GPIO.input(12) == False):
        helper_count()
        notif("Bahaya",jam)
        with open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama,thn,bln)) as json_file:
            data = json.load(json_file)
            wrjsn = data["{}".format(tgl)]        
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
            else:
                print("Tombol Telah Ditekan")
                break
    else:
        print("Status Aman")

    import Scripts.aquanotif
    time.sleep(0.5)

    if jam == "00:00":
        s1 = 0
        s2 = 0