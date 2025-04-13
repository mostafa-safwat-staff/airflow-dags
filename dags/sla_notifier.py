from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import airflow.utils.dates
from airflow.utils.email import send_email
import datetime

def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis, *args, **kwargs):
    send_email(
        to=["mostafa.safwat.staff@gmail.com"],
        subject="[Airflow SLA Miss] Task missed its SLA",
        html_content=f"""
        <p>SLA was missed on the following tasks: {task_list}</p>
        <p>Blocking tasks: {blocking_task_list}</p>
        <p>SLAs: {slas}</p>
        <p>Blocking TIs: {blocking_tis}</p>
        """
    )


dag = DAG (
    dag_id = "sla_notifier",
    default_args={
        "email": "mostafa.safwat.staff@gmail.com" 
    },
    sla_miss_callback=sla_miss_callback,
    schedule_interval=datetime.timedelta(minutes=3),
    start_date=datetime.datetime(2025, 1, 1, 12),
    end_date=datetime.datetime(2026, 1, 1, 15),
)

sleeptask = BashOperator(
    task_id="sleeptask",
    bash_command="sleep 65",
    sla=datetime.timedelta(minutes=1),
    dag=dag,
)