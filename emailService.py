import mysql.connector
import smtplib
from email.message import EmailMessage

SMTP_SERVER = 'smtp.hostinger.com'
SMTP_PORT = 465
SENDER_EMAIL = 'contact@lionelcassar.info'
SENDER_PASSWORD = 'Hubble2024!'

def get_data_from_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='cessi'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM email_test WHERE email IS NOT NULL")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def send_emails(data):
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Iniciar sesión

            for d in data:
                email_dest = d[1]
                empresa = d[2]  # Asegúrate de que el índice sea el correcto
                body = f"Este es el cuerpo del correo electrónico que se enviará a {empresa}."

                msg = EmailMessage()
                msg.set_content(body)
                msg['Subject'] = "Asunto del correo"
                msg['From'] = SENDER_EMAIL
                msg['To'] = email_dest

                server.send_message(msg)  # Enviar el correo

            print("Todos los correos han sido enviados correctamente.")
        
    except smtplib.SMTPAuthenticationError:
        print("Error de autenticación. Verifica tus credenciales.")
    except smtplib.SMTPConnectError:
        print("Error de conexión al servidor SMTP. Verifica el servidor y el puerto.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    data = get_data_from_db()
    send_emails(data)
