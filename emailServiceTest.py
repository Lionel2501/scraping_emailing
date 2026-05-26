import os
from pathlib import Path
import smtplib
from email.message import EmailMessage

from mail_config import get_smtp_config


SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD = get_smtp_config()
TEST_EMAIL = os.getenv("TEST_EMAIL", SENDER_EMAIL)
PDF_PATH = Path(__file__).resolve().parent / "Lionel Cassar - Desarrollador Full-stack.pdf"


def send_test_email():
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)

            empresa = "Empresa Test"
            body = f"""\
Estimado/a,

Me comunico con ustedes para expresar mi interes en una vacante de programador en {empresa}.

Adjunto mi curriculum, donde detallo mi experiencia laboral, habilidades y proyectos anteriores.

Actualmente me encuentro preparado para asumir nuevas responsabilidades, aportar soluciones concretas y contribuir activamente al desarrollo de proyectos y objetivos de la empresa.

Estoy a disposicion para coordinar una entrevista o llamada telefonica en caso de que requieran mas informacion.

Atentamente,
Lionel Cassar
"""

            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = f"Solicitud de empleo en {empresa}"
            msg["From"] = SENDER_EMAIL
            msg["To"] = TEST_EMAIL

            with PDF_PATH.open("rb") as pdf_file:
                pdf_data = pdf_file.read()
                msg.add_attachment(
                    pdf_data,
                    maintype="application",
                    subtype="pdf",
                    filename="Lionel_Cassar_CV.pdf",
                )

            server.send_message(msg)
            print(f"Email enviado correctamente a {TEST_EMAIL}")

    except smtplib.SMTPAuthenticationError:
        print("Error de autenticacion SMTP.")
    except smtplib.SMTPConnectError:
        print("Error de conexion SMTP.")
    except FileNotFoundError:
        print(f"PDF no encontrado: {PDF_PATH}")
    except ValueError as error:
        print(str(error))
    except Exception as error:
        print(f"Ocurrio un error: {error}")


if __name__ == "__main__":
    send_test_email()
