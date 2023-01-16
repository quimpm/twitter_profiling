FROM apache/airflow:latest-python3.9
COPY requirements.txt /requirements.txt
USER root
RUN apt-get update && apt-get install build-essential -y
USER airflow
RUN mkdir /home/airflow/.cache
RUN chmod -R 777 /home/airflow
ENV NUMBA_CACHE_DIR=/tmp
ENV DEVELOPMENT_MODE=False
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
RUN pip3 install --user --upgrade pip
RUN pip3 install --no-cache-dir --user -r /requirements.txt
