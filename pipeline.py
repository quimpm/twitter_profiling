from airflow import DAG
import sys
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from tasks import build_corpus, collect_statistics, image_captioning, \
 scrape_task, save_profile, keyword_extraction
from uuid import uuid1


default_args = {
    'owner': 'Quim 10^-12',
    'depends_on_past': True,
    'wait_for_downstream': True,
    'start_date': datetime.now(),
    'email': ['qpico99@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG('twitter_profiling', default_args=default_args, schedule=None)

execution_id = uuid1()

tweet_scraping_task = PythonOperator(
    task_id='tweet_scraping',
    python_callable=scrape_task.run,
    op_args=[sys.argv[0], execution_id],
    dag=dag)


image_captioning_task = PythonOperator(
    task_id='image_captioning',
    python_callable=image_captioning.run,
    op_args=[execution_id],
    dag=dag)


build_corpus_task = PythonOperator(
    task_id='build_corpus',
    python_callable=build_corpus.run,
    op_args=[execution_id],
    dag=dag)

keyword_extraction_task = PythonOperator(
    task_id='keyword_extraction',
    python_callable=keyword_extraction.run,
    op_args=[execution_id],
    dag=dag)

collect_statistics_task = PythonOperator(
    task_id='collect_statistics',
    python_callable=collect_statistics.run,
    op_args=[execution_id],
    dag=dag)

save_profile_task = PythonOperator(
    task_id='save_profile_details',
    python_callable=profile_details.run,
    op_args=[execution_id],
    dag=dag)


image_captioning_task.set_upstream(tweet_scraping_task)
collect_statistics_task.set_upstream(tweet_scraping_task)
build_corpus_task.set_upstream(image_captioning_task)
keyword_extraction_task.set_upstream(build_corpus_task)
save_profile_task.set_upstream(keyword_extraction_task)
save_profile_task.set_upstream(collect_statistics_task)
