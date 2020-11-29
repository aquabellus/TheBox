import mysql.connector, json, datetime, logging, re
from time import sleep
import mysql.connector.errors as errors

logging.basicConfig(filename='log/aqualog.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

json_setup = json.loads(open("setup.json").read())

def insert_db(timestamp, status, tinggi, jam):
    tgl = datetime.datetime.now().strftime("%Y/%m/%d")
    db = mysql.connector.connect(
    host=json_setup["host"],
    user=json_setup["user"],
    passwd=json_setup["passwd"],
    database=json_setup["database"],
    auth_plugin=json_setup["auth"]
    )

    cursor = db.cursor()
    sql = "INSERT INTO BoxDump (timestamp, tanggal, status, tinggi, jam) VALUES (%s, %s, %s, %s, %s)"
    val = (timestamp, tgl, status, tinggi, jam)
    cursor.execute(sql, val)
    db.commit()
    print("Status {} Pukul {} Telah Berhasil Ditambahkan".format(status, jam))

def validate_db():
    db = mysql.connector.connect(
    host=json_setup["host"],
    user=json_setup["user"],
    passwd=json_setup["passwd"],
    auth_plugin=json_setup["auth"],
    database=json_setup["database"]
    )

    cursor = db.cursor()
    cursor.execute("SELECT * from BoxDump ORDER BY id DESC LIMIT 1")
    data = cursor.fetchall()
    baca = json.dumps(data, indent=4)
    try:
        return(re.search(r"\d{14}", baca).group())
    except:
        return(False)

def sync_db(nama, thn, tgl):
    buka = open("/home/{}/Documents/BoxDump.d/{}/{}.json".format(nama, thn, tgl))
    baca = buka.read()
    urai = json.loads(baca)
    cari = re.findall(r"\d{10}", baca)
    hitung = len(cari)
    ambil = urai[re.search(r"\d+\/\d+\/\d+", baca).group()][int(hitung) - 1]
    kunci = re.search(r"\d{12}", str(ambil)).group()
    try:
        re.search(kunci + r"\d{2}", str(validate_db())).group()
    except(AttributeError):
        insert_db(ambil["Timestamp"], ambil["Status"], ambil["Tinggi"], ambil["Jam"])

def create_db():
    db = mysql.connector.connect(
    host=json_setup["host"],
    user=json_setup["user"],
    passwd=json_setup["passwd"],
    auth_plugin=json_setup["auth"]
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
    database=json_setup["database"],
    auth_plugin=json_setup["auth"]
    )

    cursor = db.cursor()
    sql = """CREATE TABLE BoxDump (
        id INT NOT NULL AUTO_INCREMENT,
        timestamp VARCHAR(14),
        tanggal VARCHAR(16),
        status VARCHAR(32),
        tinggi VARCHAR(16),
        jam VARCHAR(16),
        PRIMARY KEY (id)
    )
    """
    cursor.execute(sql)
    print("Tabel BoxDump Telah Berhasil Dibuat")

if __name__ == "__main__":
    try:
        create_db()
    except(errors.DatabaseError):
        print("Database sudah tersedia\n")
        try:
            tabel_db()
        except(errors.ProgrammingError):
            print("Tabel sudah tersedia")
    except:
        logging.warning('This will get logged to a file')
    else:
        tabel_db()