import mysql.connector, json, datetime, logging, os
from time import sleep

json_setup = json.loads(open("setup.json").read())

if os.path.exists("log/") == False:
    os.mkdir("log/")
logging.basicConfig(filename='log/aquasetup.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def insert_db(status):
    jam = datetime.datetime.now().strftime("%H:%M:%S")
    thn = datetime.datetime.now().strftime("%Y/%m/%d")
    db = mysql.connector.connect(
    host=json_setup["host"],
    user=json_setup["user"],
    passwd=json_setup["passwd"],
    database=json_setup["database"]
    )

    cursor = db.cursor()
    sql = "INSERT INTO BoxDump (thn, status, jam) VALUES (%s, %s, %s)"
    val = (thn, status, jam)
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
        tanggal DATE(),
        status CHAR(9),
        jam TIME()
    )
    """

    cursor.execute(sql)
    print("Tabel BoxDump Telah Berhasil Dibuat")

if __name__ == "__main__":
    try:
        create_db()
        tabel_db()
        print("Jalankan aquastart.py untuk memulai monitoring")
    except(SystemExit, SystemError):
        logging.warning('This will get logged to a file')
