from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import requests
import json
import logging



def print_welcome():
    print('Welcome to Airflow!')
    print('Today is {}'.format(datetime.today().date()))

def print_date():
    print('Today is {}'.format(datetime.today().date()))


def print_random_quote():
    url = "https://pokeapi.co/api/v2/pokemon/rhyhorn"
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        j = r.json()
        name = j["name"]
        logging.info(f"Pokemon Name: {name}")
        order = j["order"]
        logging.info(f'Pokemon Order: {order}')
        abilities = j["abilities"]
        logging.info("Abilities:")
        for ability in abilities:
            ability_name = ability["ability"]["name"]
            logging.info(f"- {ability_name}")
        types = j["types"]
        logging.info("Types:")
        for poke_type in types:
            logging.info(f'-{poke_type["type"]["name"]}')
    except requests.RequestException as e:
        logging.error(f"Error fetching Pokemon information: {e}") 



dag = DAG(
    'poke_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 23 * * *',
    catchup=False

)



print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=dag

)



print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag

)



print_random_quote = PythonOperator(
    task_id='print_random_quote',
    python_callable=print_random_quote,
    dag=dag

)



# Set the dependencies between the tasks

print_welcome_task >> print_date_task >> print_random_quote