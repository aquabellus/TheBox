import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.OUT)  #LED Merah
GPIO.setup(5,GPIO.OUT)  #LED Hijau
GPIO.setup(7,GPIO.OUT)  #LED Biru
GPIO.setup(8,GPIO.IN)   #Sensor Aman
GPIO.setup(10,GPIO.IN)  #Sensor Siaga I
GPIO.setup(12,GPIO.IN)  #Sensor Siaga II
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

def siagaI():
    s1 = int()
    if (GPIO.input(8) == False):
        s1 = s1 + 1
        if s1 >= 20:
            while True:
                if (GPIO.input(16) == False):
                    hijau()
                    sleep(2)
                    netral()
                    sleep(2)
                else:
                    print("Tombol telah ditekan")
                    break
        else:
            sleep(2)
    else:
        print("Cek Siaga II")
        siagaII()

def siagaII():
    s2 = int()
    if (GPIO.input(10) == False):
        s2 = s2 + 1
        if s2 >= 10:
            while True:
                if (GPIO.input(16) == False):
                    kuning()
                    sleep(1)
                    netral()
                    sleep(1)
                else:
                    print("Tombol telah ditekan")
                    break
        else:
            sleep(2)
    else:
        print("Cek Bahaya")
        bahaya()

def bahaya():
    if (GPIO.input(12) == False):
        while True:
            if (GPIO.input(16) == False):
                merah()
                sleep(0.5)
                netral()
                sleep(0.5)
            else:
                print("Tombol telah ditekan")
                break
    else:
        print("Aman")
        print("Mulai dari awal")
        
while True:
    try:
        siagaI()
        sleep(2)
    except (KeyboardInterrupt,SystemExit):
        GPIO.cleanup()