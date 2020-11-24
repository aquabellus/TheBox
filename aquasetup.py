import mysql.connector, json, datetime, logging, os
from time import sleep

json_setup = json.loads(open("setup.json").read())

if os.path.exists("log/") == False:
    os.mkdir("log/")

def insert_db(timestamp, status, tinggi):
    jam = datetime.datetime.now().strftime("%H:%M:%S")
    tgl = datetime.datetime.now().strftime("%Y/%m/%d")
    db = mysql.connector.connect(
    host=json_setup["host"],
    user=json_setup["user"],
    passwd=json_setup["passwd"],
    database=json_setup["database"]
    )

    cursor = db.cursor()
    sql = "INSERT INTO BoxDump (timestamp, tanggal, status, tinggi, jam) VALUES (%s, %s, %s, %s, %s)"
    val = (timestamp, tgl, status, tinggi, jam)
    cursor.execute(sql, val)
    db.commit()
    print("Status {} Pukul {} Telah Berhasil Ditambahkan".format(status, jam))

def create_db():
    db = mysql.connector.connect(
    host=json_setup["host"],
    user=json_setup["user"],
    passwd=json_setup["passwd"]
    )

    if db.is_connected():
        print("Koneksi Ke DataBase Berhasil !!!")
        print("Membuat DataBase Baru")
        sleep(2)

    cursor = db.cursor()
    cursor.execute("CREATE DATABASE TheBox")
    print("Database TheBox berhasil dibuat")

def tabel_db():
    print("Membuat Tabel")
    db = mysql.connector.connect(
    host=json_setup["host"],
    user=json_setup["user"],
    passwd=json_setup["passwd"],
    database=json_setup["database"]
    )

    cursor = db.cursor()
    sql = """CREATE TABLE BoxDump (
        timestamp VARCHAR(14),
        tanggal VARCHAR(16,
        status VARCHAR(32),
        tinggi VARCHAR(16),
        jam VARCHAR(16)
    )
    """

    cursor.execute(sql)
    print("Tabel BoxDump Telah Berhasil Dibuat")

if __name__ == "__main__":
    logging.basicConfig(filename='log/aquasetup.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    try:
        create_db()
        tabel_db()
    except(SystemExit, SystemError):
        logging.warning('This will get logged to a file')
