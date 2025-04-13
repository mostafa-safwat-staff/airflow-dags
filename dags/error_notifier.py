from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import airflow.utils.dates

def send_error():
    print("ERROR!")

dag = DAG (
    dag_id = "error_notifier",
    schedule_interval=None, 
    start_date=airflow.utils.dates.days_ago(3),
    default_args={"on_failure_callback": send_error, "email": "mostafa.safwat.1@gmail.com"},
    on_failure_callback=send_error
)

failing_task = BashOperator(
    task_id="failing_task",
    bash_command="exit 1",
    dag=dag,
)

# sleeptask = BashOperator(
#     task_id="sleeptask",
#     bash_command="sleep 60",
#     sla=datetime.timedelta(minutes=2),
#     dag=dag,
# )