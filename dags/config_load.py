import os
import yaml
from airflow import DAG
from airflow.operators.python import PythonOperator

dag_file_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(dag_file_dir, 'config', 'dag.prod.yaml')


with open(config_file, 'r') as config_file:
    config = yaml.safe_load(config_file)


def config_load(input_path, output_path):
    print(">>> config paths: ", input_path, output_path)


with DAG(
    "config_load",
    schedule=None,
    catchup=False,
) as dag:

    check_version = PythonOperator(
        task_id="log_python_version",
        op_kwargs={
            "input_path": config["input_path"],
            "output_path": config["output_path"],
        },
        python_callable=config_load,
    )
