import RPi.GPIO as GPIO
import time
import json
import os.path
from os import path


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
    GPIO.output(3,False)
    GPIO.output(5,False)
    GPIO.output(7,False)

def merah():
    GPIO.output(3,True)
    GPIO.output(5,False)
    GPIO.output(7,False)

def kuning():
    GPIO.output(3,True)
    GPIO.output(5,True)
    GPIO.output(7,False)

def hijau():
    GPIO.output(3,False)
    GPIO.output(5,True)
    GPIO.output(7,False)

tgl = time.strftime("%d %b", time.localtime())

bln = time.strftime("%b %Y", time.localtime())

jam = time.strftime("%H:%M", time.localtime())

def write_json(data, filename=("{}.json").format(bln)):
    with open(filename, 'w') as jswrt:
        json.dump(data, jswrt, indent = 4)

tmprpt = {
    "BoxDump" : [
        {
            "{}".format(tgl) : {
                "Status" : "Mulai",
                "Jam" : jam
            }
        }
    ]
}

json_object = json.dumps(tmprpt, indent = 4)
s1 = int()
s2 = int()

while True:
    if os.path.exists(("{}.json").format(bln)) == False:
        with open(("{}.json").format(bln), "w") as outfile:
            outfile.write(json_object)
    netral()
    if (GPIO.input(8) == False):
        s1 += 1
        if s1 >= 20:
            s1 = 0
            with open(("{}.json").format(bln)) as json_file:
                data = json.load(json_file)
                wrjsn = data["BoxDump"]        
                s1rpt = {
                    "{}".format(tgl) : {
                        "Status" : "Siaga I",
                        "Jam" : jam
                    }
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
            print(("Status Siaga I Telah Terekam Sebanyak : {} Kali").format(s1))
    elif (GPIO.input(10) == False):
        s2 += 1
        if s2 >= 10:
            s2 = 0
            with open(("{}.json").format(bln)) as json_file:
                data = json.load(json_file)
                wrjsn = data["BoxDump"]        
                s2rpt = {
                    "{}".format(tgl) : {
                        "Status" : "Siaga II",
                        "Jam" : jam
                    }
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
            print(("Status Siaga II Telah Ditekan Sebanyak {} Kali").format(s2))
    elif (GPIO.input(12) == False):
        with open(("{}.json").format(bln)) as json_file:
            data = json.load(json_file)
            wrjsn = data["BoxDump"]        
            bhya = {
                "{}".format(tgl) : {
                    "Status" : "Bahaya",
                    "Jam" : jam
                }
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
    elif (KeyboardInterrupt,SystemExit):
        GPIO.cleanup
    else:
        print("Status Aman")
    time.sleep(5)

    if jam == "00:00":
        s1 = 0
        s2 = 0