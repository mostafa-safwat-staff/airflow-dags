from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import airflow.utils.dates
import datetime

dag = DAG (
    dag_id = "sla_notifier",
    schedule_interval=None, 
    start_date=airflow.utils.dates.days_ago(3),
    default_args={
        "email": "mostafa.safwat.staff@gmail.com" 
    }
)

sleeptask = BashOperator(
    task_id="sleeptask",
    bash_command="sleep 65",
    sla=datetime.timedelta(minutes=1),
    dag=dag,
)