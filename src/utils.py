"""Suppor functions and libraries
Author: Lauro Reyes"""
import logging
import datetime as dt
import sys
import pandas as pd
import requests
import yaml
# get num and categorical columns
def read_configuration(config_file=".config.yaml"):
    """
    Read and load configuration from a YAML file.

    Args:
        config_file (str, optional): Path to the YAML configuration file. Defaults to "config.yaml".

    Returns:
        dict: Loaded configuration as a dictionary.

    Raises:
        FileNotFoundError: If the specified configuration file is not found.
        yaml.YAMLError: If there is an error in parsing the YAML file.
    """
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            logging.info("Yaml config found and read successfully.")
            return config
    except FileNotFoundError as e:
        logging.error("Failed to load configuration file: %s",e)
        sys.exit()
    except yaml.scanner.ScannerError as e:
        logging.error("Yaml config file has errors: %s",e)
        sys.exit()

def obtener_info_banxico(indicador, fecha_inicio, fecha_fin, token_api):
    """
    Esta función consulta el tipo de cambio de un indicador específico en el rango de fechas dado,
    utilizando la API del Banco de México.

    Args:
        indicador (str): El identificador del indicador a consultar.
        fecha_inicio (str): La fecha de inicio del rango de consulta en formato 'dd/mm/aaaa'.
        fecha_fin (str): La fecha de fin del rango de consulta en formato 'dd/mm/aaaa'.
        token_api (str): El token de acceso para la API del Banco de México.

    Returns:
        pd.DataFrame: Un DataFrame con las fechas y los valores correspondientes al tipo de cambio,
                      o None si hay un error en la consulta.
    """
    # Construcción de la URL para la consulta de la API
    endpoint = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{indicador}/datos/{fecha_inicio}/{fecha_fin}'

    # Configuración de los headers con el token de acceso
    headers = {'Bmx-Token': token_api}

    # Realización de la consulta GET a la API
    respuesta = requests.get(endpoint, headers=headers)

    # Verificación de la respuesta exitosa de la API
    if respuesta.status_code == 200:
        # Procesamiento de los datos recibidos en formato JSON
        datos_json = respuesta.json()
        serie_datos = datos_json['bmx']['series'][0]['datos']
        
        # Creación del DataFrame y ajuste de tipos de datos
        df = pd.DataFrame(serie_datos)
        df['dato'] = df['dato'].astype(float)  # Conversión de la columna 'dato' a float
        df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)  # Asegurar el formato correcto de la fecha
        # pasar a datos mensuales
        df['mes'] = (
            df
            .fecha
            .apply(lambda d: dt.date(d.year,d.month,1))
        )
        df = (
            df
            .sort_values(['mes','fecha'])
            .drop_duplicates(subset='mes')
            .drop(columns=['fecha'])
            .rename(columns={'mes':'fecha'})
            [['fecha','dato']]
        )
        
        return df
    else:
        # Manejo de errores en caso de respuesta no exitosa
        error_msg = f"Error al consultar el indicador {indicador}. Código de respuesta: {respuesta.status_code}"
        print(error_msg)
        return None
    
def obtener_inflacion_inegi(token):
    """
    Función para obtener datos de un indicador específico del INEGI.

    Args:
        indicador (str): El identificador del indicador a consultar.
        token (str): El token de acceso para la API del INEGI.

    Returns:
        dict: Datos obtenidos de la API en formato JSON.
    """
    # Construcción de la URL para la consulta de la API
    url = f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/539368/es/0700/false/BIE/2.0/{token}?type=json'

    # Realización de la consulta GET a la API
    response = requests.get(url)

    # Verificación de la respuesta exitosa de la API
    if response.status_code == 200:
        # Procesamiento y retorno de los datos recibidos en formato JSON
        # transformar en DF
        df = pd.DataFrame(response.json().get('Series')[0].get('OBSERVATIONS'))
        df = (
            df
            .rename(columns={'TIME_PERIOD':'fecha'})
            .drop(columns=['OBS_EXCEPTION', 'OBS_STATUS', 'OBS_SOURCE',
            'OBS_NOTE', 'COBER_GEO'])
        )
        # data types
        df['fecha'] = pd.to_datetime(df['fecha'])
        df.OBS_VALUE = df.OBS_VALUE.astype(float)
        # cambiar a dia 15
        df.fecha = df.fecha.apply(lambda d: d if d.day == 1 else d.replace(day=15))
        df = df.sort_values('fecha')
        df['dato'] = df.OBS_VALUE.pct_change(24)
        df = (
            df
            .drop(df[df.dato.isna()].index)
            .drop(columns=['OBS_VALUE'])    
        )
        return df
    else:
        # Manejo de errores en caso de respuesta no exitosa
        print(f"Error en la solicitud: Código de estado {response.status_code}")
        return None
