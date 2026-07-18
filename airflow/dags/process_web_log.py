from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# 1. Define default arguments
default_args = {
    'owner': 'Omar Ragab Hamdy',
    'start_date': datetime(2026, 7, 19),
    'email': ['omar@example.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# 2. Initialize the DAG
dag = DAG(
    'process_web_log',
    default_args=default_args,
    description='Capstone Project Web Log Pipeline',
    schedule_interval=timedelta(days=1),
)

# Task 1: Extract (Extract IP addresses using cut)
extract_data = BashOperator(
    task_id='extract_data',
    bash_command='cut -d" " -f1 /home/project/access.log > /home/project/extracted_data.txt',
    dag=dag,
)

# Task 2: Transform (Filter out local traffic 127.0.0.1 using grep)
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='grep -v "127.0.0.1" /home/project/extracted_data.txt > /home/project/transformed_data.txt',
    dag=dag,
)

# Task 3: Load (Archive the transformed data into a tar.gz file)
load_data = BashOperator(
    task_id='load_data',
    bash_command='tar -czvf /home/project/weblog.tar.gz /home/project/transformed_data.txt',
    dag=dag,
)

# Define pipeline workflow
extract_data >> transform_data >> load_data