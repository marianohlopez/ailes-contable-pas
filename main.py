from db import connect_db
from extract import extract_cont_pas
from transform import generar_mails_pas

def main():

  conn = connect_db()
  cursor = conn.cursor()
  data_pas = extract_cont_pas(cursor)
  generar_mails_pas(data_pas)

if __name__ == "__main__":
  main()