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

# Ejecutar la consulta
cursor.execute("SELECT website FROM main WHERE email IS NULL")
data = cursor.fetchall()

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()

# Guardar los datos en un archivo CSV
with open('email_empty.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['website'])  # Encabezado
    writer.writerows(data)  # Escribir todos los datos obtenidos

print('Datos guardados en email_empty.csv')

