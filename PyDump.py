import mysql.connector

conn = mysql.connector.connect(host="localhost",database="parts_test2",user="data0",password="XXfish3x3")

curs=conn.cursor()
#curs.execute("SHOW DATABASES")
#for db in curs:
#    print(db)

uidCol = []
descCol = []

cnt=0
curs.execute("SELECT U_ID FROM dummytest WHERE TYPE='ASS'")
for row in curs:
    uidCol.append(row)
    cnt+=1

cnt=0
curs.execute("SELECT LABEL FROM dummytest WHERE TYPE='ASS'")
for row in curs:
    descCol.append(row)
    cnt+=1

for i in range(cnt):
    dummy=uidCol[i]
    dumpStr=
    print(dummy)
conn.close()
    
