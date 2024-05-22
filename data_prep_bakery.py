import pandas as pd
from sklearn.model_selection import train_test_split
import boto3
from io import StringIO

# Leer datos de ventas en formato Parquet desde S3
bakery_data_path = 's3://bakery-project/clean_bakery_sales.parquet'
bakery_df = pd.read_parquet(bakery_data_path, engine='pyarrow')

# Convertir la columna 'Date' a formato datetime
bakery_df['Date'] = pd.to_datetime(bakery_df['Date'])
bakery_df['Month'] = bakery_df['Month'].str.replace('-', '')

# Convertir la columna 'Menu' a formato numerico
bakery_df['Menu_Code'] = pd.Categorical(bakery_df['Menu']).codes

# Crear un DataFrame con los códigos de menú
df_menu = bakery_df[['Menu_Code', 'Menu', 'Price']]
df_menu = df_menu.drop_duplicates(subset=['Menu_Code', 'Menu'])

# Leer datos de Temperatura
weather_data_path = './raw_data/TempTot.csv'
weather_df = pd.read_csv(weather_data_path)

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

# Imprimir la longitud de cada conjunto de datos
print("Tamaño del conjunto de entrenamiento:", len(train_df))
print("Tamaño del conjunto de validación:", len(val_df))
print("Tamaño del conjunto de prueba:", len(test_df))
print("Tamaño del conjunto de menú:", len(df_menu))

# Convertir los DataFrames a formato CSV
train_df.to_csv('train.csv', index=False)
val_df.to_csv('val.csv', index=False)
test_df.to_csv('test.csv', index=False)
df_menu.to_csv('menu_codes.csv', index=False)

# Establecer conexión con S3
s3 = boto3.client('s3',
                  aws_access_key_id='YUNYUNYUN',
                  aws_secret_access_key='YUNYUNYUNYUNYUNYUN')

# Especificar el nombre del bucket de S3 y los nombres de los archivos
bucket_name = 'bakery-project'
train_file_key = 'data/train.csv'
val_file_key = 'data/validation.csv'
test_file_key = 'data/test.csv'
menu_codes_key = 'data/menu_codes.csv'

# Subir los archivos CSV a S3
s3.upload_file('train.csv', bucket_name, train_file_key)
s3.upload_file('val.csv', bucket_name, val_file_key)
s3.upload_file('test.csv', bucket_name, test_file_key)
s3.upload_file('menu_codes.csv', bucket_name, menu_codes_key)

print("Archivos CSV guardados en S3 exitosamente.")
