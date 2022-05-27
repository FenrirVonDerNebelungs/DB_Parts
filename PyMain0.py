import mysql.connector

conn = mysql.connector.connect(host="localhost",database="parts_test2",user="data0",password="pppp");

curs=conn.cursor();
curs.execute("SHOW DATABASES")
for db in curs:
    print(db)

