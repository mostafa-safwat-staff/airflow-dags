from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

def log_python_version():
    print("Python version:", sys.version)

with DAG("check_python_version",
         start_date=datetime(2024, 1, 1),
         schedule_interval=None,
         catchup=False) as dag:

    check_version = PythonOperator(
        task_id="log_python_version",
        python_callable=log_python_version,
    )