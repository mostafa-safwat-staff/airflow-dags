from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import airflow.utils.dates

def send_error():
    print("ERROR!")

dag = DAG (
    dag_id = "sla_notifier",
    schedule_interval=None, 
    start_date=airflow.utils.dates.days_ago(3),
    default_args={
        "on_failure_callback": send_error, 
        "email": "mostafa.safwat.staff@gmail.com", 
        "email_on_failure": True, 
        "email_on_retry": False, 
    },
    on_failure_callback=send_error
)

sleeptask = BashOperator(
    task_id="sleeptask",
    bash_command="sleep 65",
    sla=datetime.timedelta(minutes=1),
    dag=dag,
)