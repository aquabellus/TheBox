import telegram, json, mysql.connector, re

template = {
    "host" : "HOST / IP SERVER",
    "user" : "USER SERVER",
    "passwd" : "PASSWORD SERVER",
    "database" : "DATABASE NAME SERVER",
    "token" : "TOKEN TELEGRAMBOT",
    "chatid" : "CHAT ID",
    "SI" : "FIRST HEIGHT",
    "SI/II" : "FIRST/SECOND HEIGHT",
    "SII" : "SECOND HEIGHT",
    "SII/B" : "SECOND/DANGER HEIGHT",
    "B" : "DANGER HEIGHT"
}

configuration = {
    "host" : "YOUR HOST",
    "user" : "YOUR USERNAME",
    "passwd" : "YOUR PASSWORD",
    "token" : "YOUR TOKEN",
    "chatid" : "YOUR CHAT ID"
}

config_dump = json.dumps(configuration, indent=4)
saring = re.sub("[^A-Z]", " ", config_dump)

def check_bot():
    try:
        checkBot = telegram.Bot(configuration["token"])
        checkBot.sendMessage(configuration["chatid"], "Bot Check Is Passed")
    except:
        if re.search(r"YOUR\s\w+", saring):
            return("Field is not configured")
        else:
            return("Error")
    return("OK")

def check_json():
    try:
        json.loads(open("./setup.json").read())
    except(FileNotFoundError):
        return("File not found")
    except:
        return("Error")
    return("OK")

def check_database():
    try:
        db = mysql.connector.connect( host=configuration["host"], user=configuration["user"], passwd=configuration["passwd"] )
        db.is_connected()
    except:
        if re.search(r"YOUR\s\w+", saring):
            return("Field is not configured")
        else:
            return("Error")
    return("OK")

print("#########################")
print("#                       #")
print("#   Aqua File Checker   #")
print("#                       #")
print("#########################")
print("")
print("")
print("Bot Status : {}".format(check_bot()))
print("JSON Status : {}".format(check_json()))
print("Database Status : {}".format(check_database()))