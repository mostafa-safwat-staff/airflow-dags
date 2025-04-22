FROM apache/airflow:2.10.5

# Copy the requirements file for DAGs
COPY ./dags/requirements.txt .

# Copy webserver config
COPY ../config/webserver_config.py /opt/airflow/webserver_config.py

# Copy the packages directory
COPY ./packages /tmp/packages/

# Install requirements and the custom package
RUN pip install --no-cache-dir -r requirements.txt && \
    find /tmp/packages -type d -maxdepth 1 -mindepth 1 -exec pip install --no-cache-dir {} \;
