import os, datetime, time,re, psutil, logging

if os.path.exists("log/") == False:
    os.mkdir("log/")
if os.path.exists("helper/") == False:
    os.mkdir("helper/")

from aquabot import check, minute_count, notif
from aquastart import cek, nama

logging.basicConfig(filename='log/aqualog.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

def check_bot():
    get_process = os.popen("ps ax | grep aquabot.py | grep -v grep").read()
    try:
        pid = re.search(r"\d+", get_process).group()
    except:
        return(False)
    return(pid)

def bot_try():
    now = datetime.datetime.now().strftime("%M")
    b = int(now) + 2
    if b >= 60:
        b -= 60
    return(b)

def main():
    a = 0
    b = bot_try()
    while True:
        if os.path.exists("log/aqualog.log") == False:
            open("log/aqualog.log", "w+")
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
            b = 0
        print("")
        if check() == False:
            print("Trigger Script Tidak Terdeteksi")
            print("Pengecekan Ulang Akan Dilakukan Pada Menit Ke {}".format(a))
        else:
            print("Trigger Script Terdeteksi")
            print("Notifikasi Akan Dikirimkan Seketika Apabila Script Tidak Terdeteksi/Berhenti")
        time.sleep(1)
        os.system("clear")

if __name__ == "__main__":
    try:
        main()
    except:
        logging.warning("This will get logged to a file")