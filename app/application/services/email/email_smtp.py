from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.utils.schemas.email_config_shema import email_settings
from typing import List


conf = ConnectionConfig(
    MAIL_USERNAME=email_settings.MAIL_USERNAME,
    MAIL_PASSWORD=email_settings.MAIL_PASSWORD,
    MAIL_FROM=email_settings.MAIL_FROM,
    MAIL_FROM_NAME=email_settings.MAIL_FROM_NAME,
    MAIL_PORT=email_settings.MAIL_PORT,
    MAIL_SERVER=email_settings.MAIL_SERVER,
    USE_CREDENTIALS=email_settings.USE_CREDENTIALS,
    VALIDATE_CERTS=email_settings.VALIDATE_CERTS,
    MAIL_STARTTLS=email_settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=email_settings.MAIL_SSL_TLS
)


class EmailService:
    def __init__(self):
        self.mail = FastMail(conf)

    async def send_email(self, subject: str, recipients: List[str], activation_code: str, name_user: str):
        html_template = '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Correo</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
    }}

    .container {{
      width: 100%;
      max-width: 600px;
      margin: 0 auto;
      background-color: rgba(0, 0, 0, 0.123);
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}

    .title {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    label {{
        font-size: 25px;
        font-weight: bold;
      color: #333;
      text-align: center;
      color: green;
    }}

    p {{
      color: #666;
      line-height: 1.6;
    }}

    strong {{
        color: green;
    }}

    label span {{
        color: orange;
    }}

    .code-box span {{
        color: green;
    }}

    .code-box {{
      display: flex;
      justify-content: center;
      gap: 15px; /* Espacio entre los caracteres */
      padding: 15px;
      font-size: 24px;
      font-weight: bold;
      border-radius: 4px;
      color: #333;
      margin: 20px 0;
    }}

    .code-box span {{
      display: inline-block;
      border-bottom: 3px solid orange;
      padding: 0 5px;
      text-align: center;
      line-height: 1; /* Asegura que el carácter quede alineado verticalmente */
    }}

    .footer {{
      margin-top: 30px;
      font-size: 16px;
      color: #333;
    }}

    .signature {{
      border-top: 1px solid orange;
      padding-top: 20px;
      margin-top: 30px;
    }}

    .signature-container {{
      display: flex;
      align-items: center;
      justify-content: left;
    }}

    .signature img {{
      border-radius: 50%;
      width: 100px;
      height: 100px;
    }}

    .signature-divider {{
      height: 150px; /* Igual a la altura de la imagen */
      width: 1px;
      background-color: orange;
      margin: 0 15px;
    }}

    .signature-text {{
      text-align: left;
      line-height: 1.2; /* Espaciado reducido para más compacidad */
    }}

    .signature-name {{
      font-size: 18px;
      font-weight: bold;
      margin: 0;
      color: green;
      padding-bottom: 3px; /* Ajusta la separación entre el nombre y el cargo */
    }}

    .signature-role {{
      font-size: 14px;
      color: #666;
      margin-bottom: 5px;
    }}

    .signature-info {{
      font-size: 14px;
      color: #333;
    }}

    .signature-info span {{
      display: block;
    }}

    .signature-year {{
      font-size: 12px;
      color: #888;
      margin-top: 10px;
    }}

    /* Media Queries para móviles */
    @media screen and (max-width: 600px) {{
      .container {{
        width: 90%;
        padding: 15px;
      }}

      .signature-container {{
        flex-direction: column; /* Coloca la imagen y el texto uno debajo del otro */
        align-items: center;
      }}

      .signature-divider {{
        display: none; /* Esconde la línea divisora en pantallas pequeñas */
      }}

      .signature img {{
        margin-bottom: 10px; /* Añade un margen debajo de la imagen para separarla del texto */
      }}

      .code-box {{
        font-size: 20px;
        padding: 25px;
      }}

      .code-box span {{
        padding: 0 1px;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="title">
        <label><span>¡</span>Bienvenido a Nuestro Servicio<span>!</span></label>
    </div>
    <p>Hola <strong>{name}</strong>👋,</p>
    <p>Gracias por unirte a nosotros😊. Estamos encantados de tenerte a bordo🚀. Para completar tu registro, utiliza el siguiente👇 código de confirmación:</p>
    <div class="code-box">
      {code}
    </div>
    <p>Introduce este código en la página de verificación para confirmar tu cuenta✅.</p>
    <p>Si no solicitaste esta cuenta🫤, por favor ignora este mensaje.</p>
    <p>Saludos cordiales🤗,</p>
    <div class="footer">
      <div class="signature">
        <div class="signature-container">
          <img src="https://media.licdn.com/dms/image/D4D03AQF72yK3nzstqg/profile-displayphoto-shrink_200_200/0/1683169249594?e=2147483647&v=beta&t=U5yxMtgGtA_30vOV9C4BsygyHN9A9AHXGavLW5LxzsU" alt="Firma">
          <div class="signature-divider"></div>
          <div class="signature-text">
            <p class="signature-name">Yeison Danuil Ascanio</p>
            <p class="signature-role">CEO, Nuestro Servicio</p>
            <div class="signature-info">
              <span>Teléfono: +34 123 456 789</span>
              <span>Correo: equipoTecnico@nuestroservicio.com</span>
              <span>Sitio web: www.nuestroservicio.com</span>
            </div>
            <p class="signature-year">© 2024</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
 '''

        html = html_template.format(
            name=name_user,
            code=''.join(f'<span>{char}</span>' for char in activation_code),
        )

        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=html,
            subtype=MessageType.html
        )

        await self.mail.send_message(message)
