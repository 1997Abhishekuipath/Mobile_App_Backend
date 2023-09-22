import mysql.connector

db=mysql.connector.connect(host='gsd-db',user='chatbot',password='Axsw@#$4321',database='ksubscribers',port=1433)

cursor=db.cursor()

cursor.execute("SHOW TABLES")

for table_name in cursor:
   print(table_name)
