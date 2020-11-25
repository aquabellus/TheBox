import os, datetime, time,re, psutil
from aquabot import check, minute_count, notif
from aquastart import s1, s2, s3, cek, nama

def check_bot():
    for process in psutil.process_iter():
        if process.cmdline() == ['python3', 'aquabot.py']:
            return(True)
    return(False)

def bot_try():
    now = datetime.datetime.now().strftime("%M")
    b = int(now) + 2
    if b >= 60:
        b -= 60
    return(b)


if __name__ == "__main__":
    a = 0
    b = bot_try()
    while True:
        minute = datetime.datetime.now().strftime("%M")
        if check() == False:
            if a == 0:
                notif("mati")
                a = minute_count()
            elif a == int(minute):
                notif("mati")
                a = minute_count()
        else:
            a = 0
        print("      #############################")
        print("     #                           #")
        print("    #          TheBox           #")
        print("   #   Flood Detector System   #")
        print("  #                           #")
        print(" #############################")
        print("https://github.com/aquabellus")
        print("\n"*3)
        print("Selamat Datang {}".format(nama))
        print("")
        if check_bot() == False:
            print("Bot Telegram Tidak Terdeteksi")
            if b == 0:
                print("Mencoba Memulai Ulang ...")
                os.system("lxterminal -e python3 aquabot.py")
                time.sleep(1)
                if check_bot() == True:
                    print("Bot Berhasil Dimulai Ulang")
                else:
                    print("Bot Tidak Berhasil Dimulai Ulang")
                    b = bot_try()
            elif b == int(minute):
                print("Mencoba Memulai Ulang ...")
                os.system("lxterminal -e python3 aquabot.py")
                time.sleep(1)
                if check_bot() == True:
                    print("Bot Berhasil Dimulai Ulang")
                else:
                    print("Bot Tidak Berhasil Dimulai Ulang")
            else:
                print("Bot Akan Dimulai Ulang Pada Menit Ke {}".format(b))
        else:
            print("Bot Telegram Terdeteksi")
        print("")
        if check() == False:
            print("Trigger Script Tidak Terdeteksi")
            print("Pengecekan Ulang Akan Dilakukan Pada Menit Ke {}".format(a))
        else:
            print("Trigger Script Terdeteksi")
            print("Notifikasi Akan Dikirimkan Seketika Apabila Script Tidak Terdeteksi/Berhenti")
        print("")
        print("Status JSON Dump : {}".format(cek()))
        print("Hasil Monitor :")
        print("Siaga I : {} Kali".format(s1))
        print("Siaga II : {} Kali".format(s2))
        print("Bahaya : {} Kali".format(s3))
        time.sleep(1)
        os.system("clear")