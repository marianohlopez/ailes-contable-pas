from db import connect_db
from extract import extract_cont_pas
from transform import generar_mails_pas

def main():

  conn = connect_db()
  cursor = conn.cursor()
  data_pas = extract_cont_pas(cursor)

  test = [('Jesica Soledad Mercado Furlong', 'ml.3012@gmail.com', 'ALUMNO: Lihuel Iván Iparraguirre (DNI: 50740767) PERÍODO: 07/2025 ;')
          , ('Florencia Liñan', 'mar.lopez@bue.edu.ar', 'ALUMNO: Morena Iara Polo González (DNI: 53955092) PERÍODO: 07/2025 ;')]
  generar_mails_pas(test)

if __name__ == "__main__":
  main()