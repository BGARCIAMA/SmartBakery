# prep_split_data.py
'''
En este módulo se hará el preprocesamiento de los datos
para el modelo de forecasting para SmartBakery, así como

- Este script leerá el archivo de Bakery Sales de la carpeta "raw".
- Y guardará en la carpeta de "prep" la base de datos que se ocupará
  para el modelo.
'''

import os
import logging
from datetime import datetime
import argparse
from src.scripts_prep import load_data, preprocess_data, merge_data, split_data

if not os.path.exists("logs/"):
    os.makedirs("logs/")
# Setup Logging
now = datetime.now()
date_time = now.strftime("%Y%m%d_%H%M%S")
log_prep_file_name = f"logs/{date_time}_prep.log"
logging.basicConfig(
    filename=log_prep_file_name,
    level=logging.DEBUG,
    filemode='w',  # Cambiado de 'a' a 'w' para sobrescribir los logs
    format='%(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    # Read inputs
    logging.info("Empezando el preproceso ...")
    # Se configura el parser de argumentos
    parser = argparse.ArgumentParser(
        description='Preprocessing script for bakery sales prediction model')
    parser.add_argument('--input', type=str,
                        default='./data/raw/Bakery_Sales.csv',
                        help='Path to the input data')
    parser.add_argument('--output_prep', type=str,
                        default='./data/prep',
                        help='Path to the output preprocessed data')

    # Se obtienen los argumentos proporcionados por el usuario
    args = parser.parse_args()

    logging.debug("Rutas de los datos: %s, %s",
                  args.input, args.output_prep)

    # Se asegura de que la carpeta de salida exista, si no, se crea
    if not os.path.exists(args.output_prep):
        os.makedirs(args.output_prep)

    # Se cargan los datos
    logging.info("Cargando los datos ...")
    data = load_data(args.input)
    if data is not None:
        logging.debug("Datos cargados con %d filas y %d columnas",
                      data.shape[0], data.shape[1])
        logging.info("Los datos fueron cargados correctamente")

        # Se hace el primer preprocesamiento de los datos
        logging.info("Preprocesando los datos ...")
        data = preprocess_data(
            args.input, output_prep_data=f"{args.output_prep}"
            "/data_bakery_prep.csv")
        if data is not None:
            logging.debug("Datos preprocesados con %d filas y %d columnas",
                          data.shape[0], data.shape[1])
            logging.info("Los datos fueron preprocesados correctamente")
    # Read inputs
    logging.info("Empezando la unión de bakery con temperatura ...")
    data_u, df_menu = merge_data(data, output_prep_data="data/clean_data/data_bakery_prep.csv")
    if data_u is not None:
        logging.debug("Datos unidos con %d filas y %d columnas",
                      data_u.shape[0], data_u.shape[1])
        logging.info("Los datos fueron unidos correctamente")
    # Dividir información en train, test y validation
    logging.info("Empezando la división de los datos ...")
    split_data(data_u, df_menu, output_split_data="data/clean_data/")
    logging.info("Los datos fueron divididos correctamente")
    logging.info("Fin del preproceso")
    logging.info("Los datos se encuentran en la carpeta 'data/clean_data/'")
    logging.info("Los logs se encuentran en la carpeta 'logs/'")
