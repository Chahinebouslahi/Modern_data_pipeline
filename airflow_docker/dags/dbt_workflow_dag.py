from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 31),  
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG(
    'dbt_workflow',
    default_args=default_args,
    description='Run dbt models using dbt Core',
    schedule_interval='@daily',  
    catchup=False,
)


DBT_PROJECT_DIR = "/Users/bousl/OneDrive/Documents/datapie/snowflake_dbt"  

# Task 1: Run dbt models
dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command=f'cd {DBT_PROJECT_DIR} && dbt run',
    dag=dag,
)

# Task 2: Run dbt tests after models are built
dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command=f'cd {DBT_PROJECT_DIR} && dbt test',
    dag=dag,
)

# Define task dependencies
dbt_run >> dbt_test  