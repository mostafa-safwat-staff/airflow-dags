import os
import yaml
from airflow import DAG
from airflow.operators.python import PythonOperator


def load_config():
    dag_file_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(dag_file_dir, "config", "dag.prod.yaml")

    with open(config_file, "r") as config_file:
        config = yaml.safe_load(config_file)
        return config


def print_config(**kwargs):
    ti = kwargs["ti"]  # task instance
    config = ti.xcom_pull(task_ids="load_config")
    print(f"Received from XCom: {config}")


with DAG(
    "load_config",
    schedule=None,
    catchup=False,
) as dag:

    load_config_task = PythonOperator(
        task_id="load_config",
        python_callable=load_config,
    )

    print_config_task = PythonOperator(
        task_id="print_config",
        python_callable=print_config,
        provide_context=True
    )

    load_config_task >> print_config_task
