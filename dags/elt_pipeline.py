from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

from modules.elt.load import load_data_to_db
from modules.database import init_db
from modules.extract_data import *

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 2, 17),
    "retries": 0,
    # "retry_delay": timedelta(minutes=5),
}


dag = DAG(
    "elt_pipeline",
    default_args=default_args,
    description="ELT pipeline using Airflow",
    # schedule_interval="@daily", 
    catchup=False,
)


def download_kaggle_data():
    handler = KaggleDataHandler(dataset_name="carrie1/ecommerce-data")
    handler.download_kaggle_data()

download_task = PythonOperator(
    task_id="download_kaggle_data",
    python_callable=download_kaggle_data,
    dag=dag,
)


def load():
    handler = KaggleDataHandler(dataset_name="carrie1/ecommerce-data")
    df = handler.extract_data()
    init_db()
    load_data_to_db(df)

load_task = PythonOperator(
    task_id="load_data_to_db",
    python_callable=load,
    dag=dag,
)

sql_files = {
    "overview_index": "scripts/overview_index.sql",
    "overview_by_months": "scripts/overview_by_months.sql",
    "rfm": "scripts/rfm.sql",
    "rfm_segment_percentage": "scripts/rfm_segment_percentage.sql"
}

def read_sql_file(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(file_path, 'r') as file:
        return file.read()


tasks = {
    task_id: PostgresOperator(
        task_id=task_id,
        postgres_conn_id='postgres',
        sql=filename, 
        dag=dag
    )
    for task_id, filename in sql_files.items()
}

download_task >> load_task >> [tasks["overview_index"], tasks["overview_by_months"], tasks["rfm"]>> tasks["rfm_segment_percentage"]]
