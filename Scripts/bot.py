import telepot
import time
import os

aquaBot = telepot.Bot("1480116644:AAHAWxJ0nv7AhcOr6O_OjFpNedly3lqDxd4")
aquaBot.getMe()

def handle(msg):
    chat_id = msg["chat"]["id"]
    command = msg["text"]

    print("perintah diterima : {}".format(command))

    if a1 >= 20:
        aquaBot.sendMessage("732796378", "Siaga I")
    elif a2 >= 10:
        aquaBot.sendMessage("732796378", "Siaga II")
    elif (GPIO.input(12)) == False:
        aquaBot.sendMessage("732796378", "Bahaya !!!")

aquaBot.message_loop(handle)
print("Berikan Perintah : ")

while True:
    time.sleep(5)