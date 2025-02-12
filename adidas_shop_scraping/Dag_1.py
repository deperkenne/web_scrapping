from datetime import datetime

from airflow.example_dags.example_bash_operator import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from adidas_schuhe import shoes_scrapped
from save_data_to_db import main


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 6),
    'retries': 1,
}

@dag(
    default_args=default_args,
    description='A DAG to send and consume data from brokers',
    schedule_interval='0 22 * * *',
    catchup=False,
)



def yelp_data_pipeline():
    scrapped_data = PythonOperator(
        task_id='scrapped_data',
        python_callable = shoes_scrapped
    )
    transform_data_and_save_to_db = SparkSubmitOperator(
        task_id='transform_data_and_save_to_db',
        python_callable = main
    )

    scrapped_data  >> transform_data_and_save_to_db

dag = yelp_data_pipeline()
