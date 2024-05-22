# prep_train_data.py
'''
En este módulo se hará el preprocesamiento de los datos
para el entrenamiento del modelo de forecasting para SmartBakery

- Este script leerá el archivo de clean_bakery_sales de la carpeta "clean".
- Y guardará en la misma carpeta "clean" la base de datos que se ocupará
  para entrenar el modelo.
'''

import pandas as pd
from sklearn.model_selection import train_test_split
import boto3
import logging
from datetime import datetime
from io import StringIO
import os
import yaml

# Abrir yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Lee las credenciales de AWS desde las variables de entorno
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')

# Nombre del bucket y la clave del objeto (ruta al archivo CSV en el bucket)
bucket_name = config['bucket_name']
clean_bakery_sales_key = 'clean_data/clean_bakery_sales.csv'
temperaturas_key = 'clean_data/TempTot.csv'
access_key_id=aws_access_key_id
secret_access_key=aws_secret_access_key

# Configurar el log
now = datetime.now()
date_time = now.strftime("%Y%m%d_%H%M%S")
log_prep_file_name = f"logs/{date_time}_prep_train.log"
logging.basicConfig(
    filename=log_prep_file_name,
    level=logging.DEBUG,
    filemode='w',  # Cambiado de 'a' a 'w' para sobrescribir los logs
    format='%(name)s - %(levelname)s - %(message)s')

logging.info("Empezando procesamiento de archivos de entrenamiento...")

# Establecer conexión con S3
s3 = boto3.client('s3',
                  aws_access_key_id=access_key_id,
                  aws_secret_access_key=secret_access_key)



# Descarga el archivo clean_bakery_sales.csv' desde S3
csv_obj = s3.get_object(Bucket=bucket_name, Key=clean_bakery_sales_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')

# Usa StringIO para convertir la cadena CSV en un objeto similar a un archivo
csv_buffer = StringIO(csv_string)

# Carga el CSV en un dataframe de pandas
bakery_df = pd.read_csv(csv_buffer)

# Convertir la columna 'Date' a formato datetime
bakery_df['Date'] = pd.to_datetime(bakery_df['Date'])
bakery_df['Month'] = bakery_df['Month'].str.replace('-', '')

# Convertir la columna 'Menu' a formato numerico
bakery_df['Menu_Code'] = pd.Categorical(bakery_df['Menu']).codes

# Crear un DataFrame con los códigos de menú
df_menu = bakery_df[['Menu_Code', 'Menu', 'Price']]
df_menu = df_menu.drop_duplicates(subset=['Menu_Code', 'Menu'])

# Descarga el archivo clean_bakery_sales.csv' desde S3
csv_temperaturas_obj = s3.get_object(Bucket=bucket_name, Key=temperaturas_key)
body_temp = csv_temperaturas_obj['Body']
csv_string_temp = body_temp.read().decode('utf-8')

# Usa StringIO para convertir la cadena CSV en un objeto similar a un archivo
csv_buffer_temp = StringIO(csv_string_temp)

# Carga el CSV en un dataframe de pandas
weather_df = pd.read_csv(csv_buffer_temp)

# Convertir la columna 'Fecha' a formato datetime
weather_df['Fecha'] = pd.to_datetime(weather_df['Fecha'], format='%d/%m/%y')

# Unir los DataFrames de ventas y clima
df_joined = pd.merge(bakery_df, weather_df, left_on='Date', right_on='Fecha', how='left')

# Eliminar columnas innecesarias
df_joined = df_joined[['Quantity', 'Year', 'Month', 'Day', 'Avg_temp', 'Menu_Code']]

# Agrupar por las columnas 'fecha' y 'producto' y calcular la suma de la columna 'cantidad'
df_grouped = df_joined.groupby(['Year', 'Month', 'Day', 'Avg_temp', 'Menu_Code']).agg({'Quantity': 'sum'}).reset_index()

# Reordenar las columnas
df_grouped = df_grouped[['Quantity', 'Year', 'Month', 'Day', 'Avg_temp', 'Menu_Code']]

# Dividir el conjunto de datos en entrenamiento (80%) y prueba (20%)
train_df, test_df = train_test_split(df_grouped, test_size=0.2, random_state=42)

# Dividir el conjunto de datos de entrenamiento en entrenamiento (70%) y validación (30%)
train_df, val_df = train_test_split(train_df, test_size=0.3, random_state=42)

# Longitud de cada conjunto de datos
len_train = len(train_df)
len_val = len(val_df)
len_test = len(test_df)
len_menu = len(df_menu)

# Imprimir la longitud de cada conjunto de datos
logging.info(f"Tamaño del conjunto de entrenamiento: {len_train}")
logging.info(f"Tamaño del conjunto de validación: {len_val}")
logging.info(f"Tamaño del conjunto de prueba: {len_test}")
logging.info(f"Tamaño del conjunto de menú: {len_menu}")

# Convertir los DataFrames a formato CSV
train_df.to_csv('train.csv', index=False)
val_df.to_csv('val.csv', index=False)
test_df.to_csv('test.csv', index=False)
df_menu.to_csv('menu_codes.csv', index=False)

# Especificar el nombre del bucket de S3 y los nombres de los archivos
train_file_key = 'clean_data/train.csv'
val_file_key = 'clean_data/validation.csv'
test_file_key = 'clean_data/test.csv'
menu_codes_key = 'clean_data/menu_codes.csv'

# Subir los archivos CSV a S3
s3.upload_file('train.csv', bucket_name, train_file_key)
s3.upload_file('val.csv', bucket_name, val_file_key)
s3.upload_file('test.csv', bucket_name, test_file_key)
s3.upload_file('menu_codes.csv', bucket_name, menu_codes_key)

logging.info("Archivos CSV de entrenamiento guardados en S3 exitosamente.")