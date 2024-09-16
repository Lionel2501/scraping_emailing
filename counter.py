import mysql.connector
import csv

# Conectar a la base de datos
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='cessi'
)
cursor = conn.cursor()

emailSended = 0
emailEmpty = 0
emailFull = 0

cursor.execute("SELECT count(*) FROM main WHERE email IS NULL")
emailEmpty = cursor.fetchone()[0]

cursor.execute("SELECT count(*) FROM main WHERE send = 1")
emailSended = cursor.fetchone()[0]

cursor.execute("SELECT count(*) FROM main WHERE email IS NOT NULL")
emailFull = cursor.fetchone()[0]

tosend = emailFull - emailSended
total = emailEmpty + emailFull

cursor.close()
conn.close()


print('email total ' + str(total))
print('email full ' + str(emailFull))
print('email sended ' + str(emailSended))
print('email to send ' + str(tosend))
print('email empty ' + str(emailEmpty))
