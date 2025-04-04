import gzip
import io
import pickle
import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator
from airflow.providers.amazon.aws.operators.sagemaker import SageMakerEndpointOperator
from airflow.providers.amazon.aws.operators.sagemaker import SageMakerTrainingOperator
from sagemaker.amazon.common import write_numpy_to_dense_tensor

dag = DAG( 
    dag_id="chapter7_aws_handwritten_digits_classifier", 
    schedule_interval=None, 
    start_date=airflow.utils.dates.days_ago(3),
)

download_mnist_data = S3CopyObjectOperator( 
    task_id="download_mnist_data", 
    source_bucket_name="sagemaker-sample-data-eu-west-1", 
    source_bucket_key="algorithms/kmeans/mnist/mnist.pkl.gz", 
    dest_bucket_name="sagemaker-mnist-test-data2", 
    dest_bucket_key="mnist.pkl.gz",
    aws_conn_id="aws-airflow-s3",
    dag=dag,
)