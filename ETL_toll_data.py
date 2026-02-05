from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

# defining DAG arguments
default_args = {
    'owner': 'Stewart Ayim',
    'start_date': days_ago(0),
    'email': ['Ayimstewart0@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG
dag = DAG(
    dag_id='ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Project',
    schedule_interval=timedelta(days=1),
)

# Task 2.1: Unzip data
unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xzvf /home/project/airflow/dags/tolldata.tgz -C /home/project/airflow/dags',
    dag=dag,
)

# Task 2.2: Extract data from CSV (fields 1-4)
extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d"," -f1-4 /home/project/airflow/dags/vehicle-data.csv > /home/project/airflow/dags/csv_data.csv',
    dag=dag,
)

# Task 2.3: Extract data from TSV (fields 5-7)
extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -d$\'\\t\' -f5-7 /home/project/airflow/dags/tollplaza-data.tsv | tr "\\t" "," > /home/project/airflow/dags/tsv_data.csv',
    dag=dag,
)

# Task 2.4: Extract data from fixed width file (characters 59-68)
extract_data_from_fixed_file = BashOperator(
    task_id='extract_data_from_fixed_file',
    bash_command='cut -c59-68 /home/project/airflow/dags/payment-data.txt | tr -s " " "," > /home/project/airflow/dags/fixed_width_data.csv',
    dag=dag,
)

# Task 2.5: Consolidate extracted data
consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste -d"," /home/project/airflow/dags/csv_data.csv /home/project/airflow/dags/tsv_data.csv /home/project/airflow/dags/fixed_width_data.csv > /home/project/airflow/dags/extracted_data.csv',
    dag=dag,
)

# Task 2.6: Transform data (convert to uppercase)
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='tr "[a-z]" "[A-Z]" < /home/project/airflow/dags/extracted_data.csv > /home/project/airflow/dags/transformed_data.csv',
    dag=dag,
)

# Task 2.7: Define task pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_file >> consolidate_data >> transform_data


