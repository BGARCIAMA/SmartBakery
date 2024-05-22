"""
El siguiente módulo manda los datos
preprocesados a un bucket de S3 en AWS
"""
# Se importan las librerías necesarias
# pylint: disable = unused-import
import os
import logging
from datetime import datetime
import boto3
from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ClientError
)

# Se configura el logging
if not os.path.exists("logs/"):
    os.makedirs("logs/")
# Setup Logging
now = datetime.now()
date_time = now.strftime("%Y%m%d_%H%M%S")
log_prep_file_name = f"logs/{date_time}_s3.log"
logging.basicConfig(
    filename=log_prep_file_name,
    level=logging.DEBUG,
    filemode='w',  # Cambiado de 'a' a 'w' para sobrescribir los logs
    format='%(name)s - %(levelname)s - %(message)s'
)

# Credenciales de AWS
VAR_KEY_ID = 'AKIAQ3EGV3Y7DDFTHXM6'
VAR_ACCESS_KEY = 'R/0g0c2uS/7+1Fj8WJZ1ELEYSu+WtP27CVDGr81t'
logging.info("Credenciales de AWS cargadas correctamente")

# Set the S3 bucket name and file names
BUCKET_NAME = 'smartbakery'
FILES_TO_UPLOAD = {
    './data/clean_data/data_bakery_prep.csv': 'clean_data/data_bakery_prep.csv',
    './data/clean_data/train.csv': 'clean_data/train.csv',
    './data/clean_data/test.csv': 'clean_data/test.csv',
    './data/clean_data/val.csv': 'clean_data/val.csv',
    './data/clean_data/menu_codes.csv': 'clean_data/menu_codes.csv',
    './data/raw/TempTot.csv': 'clean_data/TempTot.csv'
}
logging.info("Archivos a subir definidos correctamente")

try:
    # Create an S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=VAR_KEY_ID,
        aws_secret_access_key=VAR_ACCESS_KEY
    )
    logging.info("Cliente S3 creado correctamente")

    # Upload the files to S3
    for local_path, s3_path in FILES_TO_UPLOAD.items():
        try:
            s3.upload_file(local_path, BUCKET_NAME, s3_path)
            logging.info("Archivo csv %s subido correctamente a S3 en %s",
                         s3_path, BUCKET_NAME)
        except FileNotFoundError:
            logging.error("Archivo no encontrado: %s", local_path)
        except NoCredentialsError as e:
            logging.error("Error de credenciales: %s", e)
        except PartialCredentialsError as e:
            logging.error("Credenciales incompletas: %s", e)
        except ClientError as e:
            logging.error("Error del cliente de AWS: %s", e)

except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
    logging.error("Error al crear el cliente de S3 o subir archivos: %s", e)
