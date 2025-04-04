import airflow
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

with DAG(dag_id="tembi-data-pipeline", start_date=airflow.utils.dates.days_ago(14), schedule_interval=None) as dag:
    # Tasks are represented as operators
    collect = BashOperator(task_id="collect-data", bash_command="echo hello")

    @task()
    def transform():
        print("transform")

    # Set dependencies between tasks
    collect >> transform
