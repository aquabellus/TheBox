import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(2,GPIO.OUT)  #LED Merah
GPIO.setup(3,GPIO.OUT)  #LED Hijau
GPIO.setup(4,GPIO.OUT)  #LED Biru
GPIO.setup(8,GPIO.IN)   #Sensor Aman
GPIO.setup(10,GPIO.IN)  #Sensor Siaga I
GPIO.setup(12,GPIO.IN)  #Sensor Siaga II
GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #Tombol
#Pin 3.3V => Pin Button

s1 = 0
s2 = 0

def tombol():
    print("Tombol telah ditekan")

def merah():
    GPIO.output(2,True)
    GPIO.output(3,False)
    GPIO.output(4,False)

def kuning():
    GPIO.output(2,True)
    GPIO.output(3,True)
    GPIO.output(4,False)

def hijau():
    GPIO.output(2,False)
    GPIO.output(3,True)
    GPIO.output(4,False)

def mulai():
    if(GPIO.input(8)==False):
        print("Mulai")
    elif(GPIO.input(8)==True):
        print("Masuk siaga I")
        siagaI()

def siagaI():
    if(GPIO.input(10)==False):
        s1 = s1 + 1
        if s1 >= 20:
            while(GPIO.input(16)==False):
                hijau()
                sleep(2)
            tombol()
            s1 = 0
        else:
            print("Dari siaga I => mulai")
    elif(GPIO.input(10)==True):
        print("Masuk siaga II")
        siagaII()

def siagaII():
    if(GPIO.input(12)==False):
        s2 = s2 + 1
        if s2 >= 10:
            while(GPIO.input(16)==False):
                kuning()
                sleep(1)
            tombol()
            s2 = 0
        else:
            print("Dari siaga II => mulai")
    elif(GPIO.input(12)==True):
        while(GPIO.input(16)==False):
            merah()
            sleep(0.5)
        tombol()

while True:
    mulai()
    sleep(2)