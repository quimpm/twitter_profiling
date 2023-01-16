from airflow import DAG
import sys
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from twitter_profiling.tasks import statistics, scrape_task, sentiment_analysis, topic_modeling, plots, build_profile
from uuid import uuid1
from twitter_profiling.model.execution import Execution
from twitter_profiling.db.db_session import session
from airflow.models.param import Param


default_args = {
    'owner': 'Quim 10^-12',
    'depends_on_past': True,
    'wait_for_downstream': True,
    'start_date': datetime.now(),
    'email': ['qpico99@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=2),
}

params = {
    "exec_id": Param(str(uuid1())),
    "num_tweets": Param(100, type="integer"),
    "username": Param("unclebobmartin")
}

dag = DAG('twitter_profiling', default_args=default_args, schedule=None, params=params)

execution_id = str(uuid1())

tweet_scraping_task = PythonOperator(
    task_id='tweet_scraping',
    python_callable=scrape_task.run,
    op_args=["{{params.username}}", "{{params.exec_id}}", "{{params.num_tweets}}"],
    dag=dag)


statistics_task = PythonOperator(
    task_id='statistics',
    python_callable=statistics.run,
    op_args=["{{params.exec_id}}"],
    dag=dag)


topic_modeling_task = PythonOperator(
    task_id='topic_modeling',
    python_callable=topic_modeling.run,
    op_args=["{{params.exec_id}}"],
    dag=dag)

sentiment_analysis_task = PythonOperator(
    task_id='sentiment_analysis',
    python_callable=sentiment_analysis.run,
    op_args=["{{params.exec_id}}"],
    dag=dag)

plots_task = PythonOperator(
    task_id='plots',
    python_callable=plots.run,
    op_args=["{{params.exec_id}}"],
    dag=dag)

build_profile_task = PythonOperator(
    task_id='build_profile',
    python_callable=build_profile.run,
    op_args=["{{params.exec_id}}"],
    dag=dag)


sentiment_analysis_task.set_upstream(tweet_scraping_task)
topic_modeling_task.set_upstream(tweet_scraping_task)
statistics_task.set_upstream(sentiment_analysis_task)
plots_task.set_upstream(topic_modeling_task)
plots_task.set_upstream(sentiment_analysis_task)
build_profile_task.set_upstream(plots_task)
build_profile_task.set_upstream(statistics_task)
