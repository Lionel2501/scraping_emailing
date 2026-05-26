from pathlib import Path
import mysql.connector
import smtplib
from email.message import EmailMessage

from mail_config import get_smtp_config


SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD = get_smtp_config()
PDF_PATH = Path(__file__).resolve().parent / "Lionel Cassar - Desarrollador Full-stack.pdf"


def get_data_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cessi",
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM main WHERE email IS NOT NULL AND send = 0 LIMIT 10")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def send_emails(data):
    ids = []

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)

            for row in data:
                ids.append(row[0])
                recipient_email = row[1]
                empresa = row[2].capitalize()
                body = f"""\
Estimado/a,

Espero que se encuentre bien.

Me gustaría expresar mi interés en oportunidades como desarrollador web dentro de {empresa}. 

Soy Full Stack Developer con experiencia en PHP/Laravel, JavaScript, React, Next.js y desarrollo de sistemas web.

Adjunto mi currículum, donde encontrará más información sobre mi experiencia, habilidades técnicas y proyectos realizados.

Quedo a disposición para coordinar una entrevista o llamada en caso de que mi perfil pueda encajar en oportunidades actuales o futuras.

Muchas gracias por su tiempo.

Saludos cordiales,
Lionel Cassar
"""
                msg = EmailMessage()
                msg.set_content(body)
                msg["Subject"] = f"Solicitud de empleo en {empresa}"
                msg["From"] = SENDER_EMAIL
                msg["To"] = recipient_email

                with PDF_PATH.open("rb") as pdf_file:
                    pdf_data = pdf_file.read()
                    msg.add_attachment(
                        pdf_data,
                        maintype="application",
                        subtype="pdf",
                        filename="lionel_cassar_desarrollador_full_stack.pdf",
                    )

                server.send_message(msg)

        if not ids:
            print("No hay emails para enviar.")
            return

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="cessi",
        )
        cursor = conn.cursor()
        ids_placeholder = ", ".join(["%s"] * len(ids))
        update_query = f"UPDATE main SET send = 1 WHERE id IN ({ids_placeholder})"
        cursor.execute(update_query, tuple(ids))
        conn.commit()
        cursor.close()
        conn.close()

        print("Todos los correos han sido enviados correctamente.")

    except smtplib.SMTPAuthenticationError:
        print("Error de autenticacion. Verifica tus credenciales SMTP.")
    except smtplib.SMTPConnectError:
        print("Error de conexion al servidor SMTP. Verifica el servidor y el puerto.")
    except FileNotFoundError:
        print(f"PDF no encontrado: {PDF_PATH}")
    except ValueError as error:
        print(str(error))
    except Exception as error:
        print(f"Ocurrio un error: {error}")


if __name__ == "__main__":
    data = get_data_from_db()
    send_emails(data)
