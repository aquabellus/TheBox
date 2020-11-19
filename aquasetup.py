import mysql.connector, json, time
from aquabox import json_setup, db

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

def tabel_db(db):
    cursor = db.cursor()
    sql = """CREATE TABLE BoxDump (
        tanggal VARCHAR(255),
        status VARCHAR(255),
        jam VARCHAR(255)
    )
    """
    cursor.execute(sql)
    print("Tabel BoxDump Telah Berhasil Dibuat")

create_db()
tabel_db(db)

