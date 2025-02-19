from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from modules.etl.load import load_main_data_to_db, load_index_data_to_db
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
    "etl_pipeline",
    default_args=default_args,
    description="ETL pipeline using Airflow",
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

def main_data():
    handler = KaggleDataHandler(dataset_name="carrie1/ecommerce-data")
    df = handler.extract_data()
    init_db()
    load_main_data_to_db(df)

transform_and_load_main_task = PythonOperator(
    task_id="transform_and_load_main_task",
    python_callable=main_data,
    dag=dag,
)

def index_data():
    load_index_data_to_db()

transform_and_load_index_task = PythonOperator(
    task_id="transform_and_load_index_task",
    python_callable=index_data,
    dag=dag,
)

download_task >> transform_and_load_main_task >> transform_and_load_index_task