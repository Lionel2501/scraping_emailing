import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='cessi'
)

cursor = conn.cursor()

try:
    records_to_insert = [
        ('email1@example.com', 'Empresa1', 'http://website1.com'),
        ('email2@example.com', 'Empresa2', 'http://website2.com'),
        ('email3@example.com', 'Empresa3', 'http://website3.com')
    ]
    
    mySql_insert_query = "INSERT INTO main (email, empresa, website) VALUES (%s, %s, %s)"
    
    # Utiliza executemany para insertar múltiples registros
    cursor.executemany(mySql_insert_query, records_to_insert)

    conn.commit()

    print("Inserción exitosa.")

except mysql.connector.Error as err:
    print(f"Error de MySQL: {err}")

finally:
    cursor.close()
    conn.close()
