import mysql.connector

conn = mysql.connector.connect(host="localhost",database="parts_test2",user="data0",password="pppp");

curs=conn.cursor();
curs.execute("SHOW DATABASES")
for db in curs:
    print(db)

sqlcom = "INSERT INTO dummytest (TYPE, LABEL, QTY, INTERNALREF, COST, SALESPRICE) VALUES (%s, %s, %s, %s, %s, %s)"
valtype='PART'
vallable='unknown part'
valqty = 1
valintref=''
valcost=0.00
valsale=0.00
#valar = ("test","dummy test", 1, "nodef",0.00, 0.00)
valar=(valtype, vallable, valqty, valintref, valcost, valsale)

#sqlc = "INSERT INTO dummytest(TYPE, QTY) VALUES (%s, %s)"
#vals = ("test",2)
#curs.execute(sqlc,vals)
curs.execute(sqlcom,valar)
conn.commit()


#print(curs.rowcount, "record inserted")