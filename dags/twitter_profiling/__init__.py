import os

DB_HOST = "/Users/quimpm/uni/twitter_profiling/twitter_profiling.db" if os.getenv("DEVELOPMENT_MODE") == "True" else "/opt/airflow/twitter_profiling.db"
STATIC_FOLDER = "/Users/quimpm/uni/twitter_profiling/static/" if os.getenv("DEVELOPMENT_MODE") == "True" else "/opt/airflow/static/"
TEMPLATES_FOLDER = "/Users/quimpm/uni/twitter_profiling/twitter_profiling/templates" if os.getenv("DEVELOPMENT_MODE") == "True" else "/opt/airflow/dags/twitter_profiling/templates/"
