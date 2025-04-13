from airflow import DAG

def send_error():
    raise "Error!"

dag = DAG (
    dag_id = "error_notifier",
    schedule_interval=None, 
    start_date=airflow.utils.dates.days_ago(3),
    on_failure_callback=send_error
)