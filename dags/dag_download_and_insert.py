import os
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
from kaggle.api.kaggle_api_extended import KaggleApi

# Parâmetros do dataset do Kaggle
KAGGLE_DATASET = 'zynicide/wine-reviews'  # Substitua pelo dataset que deseja usar
KAGGLE_FILE_NAME = 'winemag-data_first150k.csv'  # Nome do arquivo CSV dentro do dataset

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1)
}
## Intanciar melhor essas credenciais
def download_kaggle_data():
    """instanciado no .env"""
    api = KaggleApi()
    api.authenticate()  # Autentica usando o kaggle.json

    # Baixa o dataset para a pasta /tmp
    api.dataset_download_files(KAGGLE_DATASET, path='/tmp', unzip=True)

def insert_data_to_postgres():
    """Insere dados do CSV baixado no PostgreSQL."""
    file_path = f'/tmp/{KAGGLE_FILE_NAME}'
    
    # Carrega o CSV em um DataFrame do pandas
    df = pd.read_csv(file_path)

    # Conecta ao PostgreSQL e insere os dados na tabela
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    pg_hook.run("CREATE TABLE IF NOT EXISTS wine_reviews (id SERIAL PRIMARY KEY, country TEXT, description TEXT, points INT, price FLOAT, variety TEXT, region TEXT);")
    
    # Insere os dados linha por linha
    for _, row in df.iterrows():
        pg_hook.run("INSERT INTO wine_reviews (country, description, points, price, variety, region) VALUES (%s, %s, %s, %s, %s, %s);",
                    parameters=(row['country'], row['description'], row['points'], row['price'], row['variety'], row['region_1']))

with DAG(
    'dag_download_and_insert',
    default_args=default_args,
    description='DAG para baixar dados do Kaggle e inserir no PostgreSQL',
    schedule_interval='@daily',
    catchup=False
) as dag:

    download_task = PythonOperator(
        task_id='download_data',
        python_callable=download_kaggle_data
    )

    insert_task = PythonOperator(
        task_id='insert_data',
        python_callable=insert_data_to_postgres
    )

    download_task >> insert_task
