from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import csv

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

def transform_data():
    """Realiza transformação simples nos dados da tabela wine_reviews e insere na tabela transformed_wine_reviews."""
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    records = pg_hook.get_records("SELECT id, country, points, price FROM wine_reviews")
    transformed_records = [(rec[0], rec[1], rec[2] * 1.1, rec[3] * 1.2 if rec[3] else None) for rec in records]  # Exemplo de transformação

    pg_hook.run("CREATE TABLE IF NOT EXISTS transformed_wine_reviews (id INT PRIMARY KEY, country TEXT, points FLOAT, price FLOAT)")
    for rec in transformed_records:
        pg_hook.run("INSERT INTO transformed_wine_reviews (id, country, points, price) VALUES (%s, %s, %s, %s);", parameters=rec)

def export_to_csv():
    """Exporta dados da tabela transformed_wine_reviews para um arquivo CSV."""
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    records = pg_hook.get_records("SELECT * FROM transformed_wine_reviews")
    with open('/usr/local/airflow/export/transformed_wine_reviews.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'country', 'points', 'price'])
        writer.writerows(records)

with DAG(
    'dag_transform_export',
    default_args=default_args,
    description='DAG para transformar dados e exportar para CSV',
    schedule_interval=None,  # Executa manualmente ou após a DAG 1
    catchup=False
) as dag:

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )

    export_task = PythonOperator(
        task_id='export_to_csv',
        python_callable=export_to_csv
    )

    transform_task >> export_task
