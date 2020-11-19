import mysql.connector, json, time

json_setup = json.loads(open("setup.json").read())

def insert_db(status):
    jam = time.strftime("%H:%M:%S", time.localtime())
    full = time.strftime("%Y/%m/%d", time.localtime())
    db = mysql.connector.connect(
    host=json_setup["host"],
    user=json_setup["user"],
    passwd=json_setup["passwd"]
    )

    cursor = db.cursor()
    sql = "INSERT INTO BoxDump (tanggal, status, jam) VALUES (%s, %s, %s)"
    val = (full, status, jam)
    cursor.execute(sql, val)
    db.commit()
    print("Status {} Pukul {} Telah Berhasil Ditambahkan".format(status, jam))

if __name__ == "__main__":
    def create_db():
        db = mysql.connector.connect(
        host=json_setup["host"],
        user=json_setup["user"],
        passwd=json_setup["passwd"]
        )

        if db.is_connected():
            print("Koneksi Ke DataBase Berhasil !!!")
            print("Membuat DataBase Baru")
            time.sleep(2)
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

    create_db()
    tabel_db()
    print("Jalankan aquastart.py untuk memulai monitoring")

