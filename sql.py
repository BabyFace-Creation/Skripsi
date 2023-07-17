import mysql.connector
from datetime import datetime

now = datetime.now()


db = mysql.connector.connect(
   host="localhost",
  user="root",
  passwd="",
  database="counter"
)

cursor = db.cursor()
sql = "INSERT INTO people (Tanggal, Jumlah) VALUES (%s, %s)"

val = (now.strftime('%Y-%m-%d %H:%M:%S'), 1)
cursor.execute(sql, val)

db.commit()

print("{} data ditambahkan".format(cursor.rowcount))