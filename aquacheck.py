import telegram, json, mysql.connector, re

template = {
    "host" : "YOUR HOST",
    "user" : "YOUR USER",
    "passwd" : "YOUR PASSWORD",
    "database" : "YOUR DATABASE",
    "token" : "YOUR TOKEN",
    "chatid" : "YOUR CHAT ID",
    "SI" : "FIRST HEIGHT",
    "SI/II" : "FIRST/SECOND HEIGHT",
    "SII" : "SECOND HEIGHT",
    "SII/B" : "SECOND/DANGER HEIGHT",
    "B" : "DANGER HEIGHT"
}

ambil = json.dumps(template, indent=4)

def check_json():
    try:
        json.loads(open("./setup.json").read())
    except(FileNotFoundError):
        open("./setup.json", "w").write(ambil)
        return("File not found")
    except:
        return("Error")
    return("OK")

def check_bot():
    try:
        checkBot = telegram.Bot(baca["token"])
        checkBot.sendMessage(baca["chatid"], "Bot Check Is Passed")
    except:
        if re.search(r"YOUR\s\w+", baca["token"]):
            return("Field is not configured")
        else:
            return("Error")
    return("OK")

def check_database():
    try:
        db = mysql.connector.connect( host=baca["host"], user=baca["user"], passwd=baca["passwd"] )
        db.is_connected()
    except:
        if re.search(r"YOUR\s\w+", baca["host"]):
            return("Field is not configured")
        else:
            return("Error")
    return("OK")

print("##########################")
print("#                        #")
print("#  Aqua Service Checker  #")
print("#                        #")
print("##########################")
print("")
print("JSON Status : {}".format(check_json()))
print("")
print("")
baca = json.loads(open("./setup.json").read())
print("Bot Status : {}".format(check_bot()))
print("Database Status : {}".format(check_database()))