# Notificador de Facturas Pendientes (PAS)

Automatización en Python desarrollada para el área Contable de una organización que brinda apoyo terapéutico y educativo a niños con discapacidad.

El script reemplaza una revisión manual mensual: identifica automáticamente qué Prestadores de Apoyo (PAS) no cargaron la factura correspondiente a sus órdenes de pago del mes y les envía un mail recordatorio con el detalle de lo adeudado, dejando registro de cada ejecución para su seguimiento.

## Stack

`Python` · `MySQL` · `MongoDB` · `yagmail (SMTP)` · `GitHub Actions`

## ¿Qué hace?

1. Se conecta a la base de datos MySQL de Ailes Inclusión.
2. Consulta la vista `v_ordenes_pago_pas` para encontrar los PAS cuya orden de pago está programada para el mes actual y que **no tienen factura cargada** (`FACTURAS IS NULL`).
3. Por cada PAS encontrado, envía un mail (vía Gmail/yagmail) recordándole que debe cargar la factura en la plataforma, incluyendo el detalle de la prestación.
4. Registra un resumen de la ejecución (cantidad de mails enviados vs. cantidad de registros encontrados) en una colección de MongoDB, para trazabilidad histórica de los reportes del área Contable.

## Estructura del proyecto

```
.
├── main.py         # Orquesta el flujo: extract -> transform -> log
├── db.py           # Conexión a MySQL y registro de reportes en MongoDB
├── extract.py      # Query de extracción de PAS con facturas pendientes
├── transform.py    # Armado y envío de los mails
├── requirements.txt
└── .github/workflows/ailes-contable-pas.yml   # Job programado de GitHub Actions
```

### `extract.py`

Ejecuta la query sobre `v_ordenes_pago_pas`, filtrando por el mes/año actual (`opa_fec_pago_prog`) y aplicando una exclusión puntual de negocio. Limpia el campo `opa_detalle` con una expresión regular para presentar la información de forma clara en el mail.

### `transform.py`

- `enviar_mail`: envía un mail individual usando `yagmail`, con asunto fijo `"Mail automatico de Contabilidad - NO CONTESTAR"` y el cuerpo con el nombre del destinatario y el detalle de la factura pendiente.
- `generar_mails_pas`: itera sobre todos los PAS obtenidos, envía el mail a cada uno y devuelve la cantidad de envíos exitosos.

### `db.py`

- `connect_db`: abre la conexión a MySQL usando `mysql.connector` con las credenciales de entorno.
- `register_report`: inserta en MongoDB un documento con timestamp (ajustado a UTC-3), área (`"Contable"`), tipo de reporte (`"pas_facturas_sin_cargar"`), cantidad de mails enviados y cantidad total de registros encontrados.

### `main.py`

Orquesta el flujo completo: conecta a la DB, extrae los PAS pendientes, envía los mails y guarda el reporte en MongoDB.

## Ejecución automática

El workflow de GitHub Actions (`.github/workflows/ailes-contable-pas.yml`) corre:

- **Automáticamente** el día 1 de cada mes a las 13:00 UTC (10:00 hora Argentina).

## Dependencias principales

- `mysql-connector-python` — conexión a MySQL
- `pymongo` — conexión a MongoDB
- `yagmail` — envío de mails vía Gmail
- `python-dotenv` — carga de variables de entorno desde `.env`

> Nota: asegurate de que estas dependencias estén listadas en `requirements.txt`.

## Notas técnicas

- El correo del remitente (`MAIL_AUTOR`) requiere una **contraseña de aplicación** de Gmail (no la contraseña habitual de la cuenta), ya que `yagmail` se autentica vía SMTP.
- Las credenciales y datos sensibles nunca se hardcodean: se inyectan por variables de entorno, tanto en local (`.env`, no versionado) como en producción (GitHub Secrets).
- Cada ejecución queda registrada en MongoDB con cantidad de mails enviados vs. registros totales, lo que permite auditar el proceso a lo largo del tiempo.
