# Análisis de la Relación entre Tasa de Interés, Tipo de Cambio e Inflación

Este repositorio contiene un conjunto de notebooks y scripts diseñados para analizar la relación entre la tasa de interés, el tipo de cambio y la inflación utilizando datos públicos de INEGI y BANXICO.

## Estructura del Repositorio

- `LICENSE`: Licencia del proyecto.
- `analytics.ipynb`: Notebook para la generación de modelos de regresión lineal.
- `data/`: Directorio que contiene los datos en formato CSV utilizados para el análisis.
- `elt.ipynb`: Notebook que crea la base de datos utilizando Amazon Glue y Amazon Athena.
- `etl.ipynb`: Notebook que descarga los datos y sube a un bucket en S3.
- `src/`: Contiene scripts de Python, incluyendo `utils.py` con funciones recurrentes utilizadas en los notebooks.

## Proceso de Análisis

El análisis se lleva a cabo en varios pasos, utilizando los notebooks proporcionados:

1. **Extracción de Datos (`etl.ipynb`)**: Descarga de datos de diversas fuentes públicas.
2. **Transformación y Carga (`elt.ipynb`)**: Creacion o modificación de los datos con Amazon Glue y Athena para preparar los datos para el análisis.
3. **Análisis (`analytics.ipynb`)**: Generación de modelos de regresión lineal para entender la relación entre la tasa de interés, el tipo de cambio y la inflación.

## Uso

Para utilizar este repositorio, se recomienda seguir los notebooks en el orden sugerido arriba. Asegúrate de tener instaladas todas las dependencias necesarias, las cuales pueden ser encontradas en los comentarios de los primeros bloques de cada notebook.

## Licencia

Este proyecto está bajo la Licencia [incluir tipo de licencia aquí]. Ver el archivo `LICENSE` para más detalles.
