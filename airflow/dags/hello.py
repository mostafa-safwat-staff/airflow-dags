import airflow
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="tembi-data-pipeline-maram", 
    start_date=airflow.utils.dates.days_ago(14), 
    schedule_interval="@daily"
    ) as dag:
    # Tasks are represented as operators
    collect = BashOperator(task_id="collect-data", bash_command="echo collect")

    transform = BashOperator(task_id="transform-data", bash_command="echo transform")

    load = BashOperator(task_id="load-data", bash_command="echo load")

    # Set dependencies between tasks
    collect >> transform >> load
