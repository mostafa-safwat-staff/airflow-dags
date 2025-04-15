import gzip
import io
import pickle
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator
import pendulum

# from airflow.providers.amazon.aws.operators.sagemaker
# import SageMakerEndpointOperator
# from airflow.providers.amazon.aws.operators.sagemaker
# import SageMakerTrainingOperator
from sagemaker.amazon.common import write_numpy_to_dense_tensor

with DAG(
    dag_id="chapter7_aws_handwritten_digits_classifier",
    schedule=None,
    start_date=pendulum.today("UTC").add(days=-3),
) as dag:
    download_mnist_data = S3CopyObjectOperator(
        task_id="download_mnist_data",
        source_bucket_name="sagemaker-sample-data-eu-west-1",
        source_bucket_key="algorithms/kmeans/mnist/mnist.pkl.gz",
        dest_bucket_name="sagemaker-mnist-test-data2",
        dest_bucket_key="mnist.pkl.gz",
        aws_conn_id="aws-airflow-s3",
        dag=dag,
    )

    def _extract_mnist_data():
        s3hook = S3Hook(aws_conn_id="aws-airflow-s3")

        # Download S3 dataset into memory
        mnist_buffer = io.BytesIO()
        mnist_obj = s3hook.get_key(
            bucket_name="sagemaker-mnist-test-data2",
            key="mnist.pkl.gz",
        )
        mnist_obj.download_fileobj(mnist_buffer)

        # Unpack gzip file, extract dataset, convert, upload back to S3
        mnist_buffer.seek(0)
        with gzip.GzipFile(fileobj=mnist_buffer, mode="rb") as f:
            train_set, _, _ = pickle.loads(f.read(), encoding="latin1")
            output_buffer = io.BytesIO()
            write_numpy_to_dense_tensor(
                file=output_buffer,
                array=train_set[0],
                labels=train_set[1],
            )

        output_buffer.seek(0)
        s3hook.load_file_obj(
            output_buffer,
            key="mnist_data",
            bucket_name="sagemaker-mnist-test-data2",
            replace=True,
        )

    extract_mnist_data = PythonOperator(
        task_id="extract_mnist_data",
        python_callable=_extract_mnist_data,
        dag=dag,
    )


download_mnist_data >> extract_mnist_data
