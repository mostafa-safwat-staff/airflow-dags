from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import airflow.utils.dates


def send_error():
    print("ERROR!")


with DAG(
    dag_id="error_notifier",
    schedule=None,
    start_date=airflow.utils.dates.days_ago(3),
    default_args={
        "on_failure_callback": send_error,
        "email": "mostafa.safwat.staff@gmail.com",
        "email_on_failure": True,
        "email_on_retry": False,
    },
    on_failure_callback=send_error,
) as dag:
    failing_task = BashOperator(
        task_id="failing_task",
        bash_command="exit 1",
        dag=dag,
    )
