import os
from dotenv import load_dotenv
import yagmail
from extract import extract_cont_pas

load_dotenv()

MAIL_AUTOR = os.getenv("MAIL_AUTOR")
APP_GMAIL_PASS = os.getenv("APP_GMAIL_PASS")

def enviar_mail(nombre, destinatario_mail, detalle):
  try:
    yag = yagmail.SMTP(MAIL_AUTOR, APP_GMAIL_PASS)
    yag.send(
      to=destinatario_mail,
      subject="Mail automatico de Contabilidad - NO CONTESTAR",
      contents= f"""Buenos días {nombre}, le informamos que aún no ha ingresado la factura correspondiente a:\n
            {detalle}\n 
            Recuerde ingresarla en la plataforma ailes.indyco.com.ar, cualquier duda comuniquese al 
            mail contable@ailesinclusion.com.ar
            \nSaludos,\n Ailes Inclusión.""",
    )
    print(f"📧 Mail enviado a {destinatario_mail}")
  except Exception as e:
    print(f"❌ Error enviando mail a {destinatario_mail}: {e}")

def generar_mails_pas(pas):

  for pa in pas:
    pa_nombre = pa[0]
    pa_mail = pa[1]
    pa_detalle = pa[2]

    enviar_mail(pa_nombre, pa_mail, pa_detalle)