def extract_cont_pas(cursor):

  query = """ 
    SELECT 
      CONCAT(pa_nombre, " ", pa_apellido) as nombre,
      pa_mail,
      REGEXP_REPLACE(opa_detalle, ' - PREST_ID: [0-9]+', '') AS opa_detalle
    FROM v_ordenes_pago_pas
    WHERE DATE_FORMAT(opa_fec_pago_prog , '%Y-%m') = DATE_FORMAT(CURDATE(), '%Y-%m')
    AND FACTURAS IS NULL
    AND pa_id != 318
   """
  cursor.execute(query)

  return cursor.fetchall()