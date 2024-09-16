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
    cursor.execute("SELECT * FROM main WHERE email IS NOT NULL AND send = 0 limit 10")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def send_emails(data):
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD) 

            ids = []
            for d in data:
                ids.append(d[0])
                email_test = d[1]
                empresa = d[2].capitalize() 
                body = f"""\
            Estimado/a,

            Me comunico con ustedes para expresar mi interés en una vacante de programador en {empresa}. 
            Adjunto mi currículum y el enlace a mi portafolio web, donde detallo mi experiencia laboral, habilidades y proyectos anteriores.

            Estoy a disposición para coordinar una entrevista o llamada telefónica en caso de que requiera más información.

            Atentamente,
            Lionel Cassar
            https://lionelcassar.info/
            """
                msg = EmailMessage()
                msg.set_content(body)
                msg['Subject'] = f"""Solicitud de empleo en {empresa}"""
                msg['From'] = SENDER_EMAIL
                msg['To'] = email_test
            
                pdf_path = './Lionel Cassar - Desarrollador Full-stack.pdf'
                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()
                    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='lionel_cassar_desarrollador_full_stack.pdf')
                
                server.send_message(msg)  
                
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='cessi'
        )
        cursor = conn.cursor()
        ids_placeholder = ', '.join(['%s'] * len(ids))

        update_query = f"UPDATE main SET send = 1 WHERE id IN ({ids_placeholder})"
        cursor.execute(update_query, tuple(ids))

        conn.commit()
        cursor.close()
        conn.close()

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
