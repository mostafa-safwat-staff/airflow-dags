FROM apache/airflow:2.10.5

COPY ./dags/requirements.txt .

COPY ../config/webserver_config.py /opt/airflow/webserver_config.py

RUN pip install --no-cache-dir -r requirements.txt
