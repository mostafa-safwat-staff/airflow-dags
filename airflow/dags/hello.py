from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

with DAG(dag_id="tembi-data-pipeline", start_date=datetime(2024, 8, 8), schedule="0 0 * * *") as dag:
    # Tasks are represented as operators
    collect = BashOperator(task_id="Collect Data", bash_command="echo hello")

    @task()
    def transform():
        print("transform")

    @task()
    def load_to_data_warehouse():
        print("load to data warehouse")

    # Set dependencies between tasks
    collect >> transform >> load_to_data_warehouse()
