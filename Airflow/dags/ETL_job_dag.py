import json
import psycopg2 as psql_connector
from datetime import datetime, timedelta

from airflow import models
from airflow.operators.python_operator import PythonOperator

from config import db_config, source_dir


def insert_data_json_to_source_db(date, **kwargs):
    conn    = psql_connector.connect(**db_config['source'])
    cur     = conn.cursor()
    
    json_data    = []
    with open(f"{source_dir}/{date}.json") as f:
        for line in f:
            json_data.append(json.loads(line))
    
    fields  = [
        'flight_date',
        'airline_code',
        'source_airport',
        'destination_airport',
        'departure_time',
        'departure_delay',
        'arrival_time',
        'arrival_delay',
        'airtime',
        'distance']

    datas = []
    for item in json_data:
        my_data = [item[field] for field in fields]
        for key, value in enumerate(my_data):
            if isinstance(value, dict):
                my_data[key] = json.dumps(value)
        datas.append(tuple(my_data))

    insert_query = "INSERT INTO flight_data(flight_date, airline_code, source_airport, destination_airport, departure_time,\
                                            departure_delay, arrival_time, arrival_delay, airtime, distance)\
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cur.executemany(insert_query, datas)
        conn.commit()
    except (Exception, psql_connector.DatabaseError) as error:
        print(error)
        """Or do something"""
        
    f.close()
    cur.close()
    conn.close()


def extract_transform_load(date, **kwargs):
    try:
        source_conn = psql_connector.connect(**db_config['source'])
        source_cur  = source_conn.cursor()
        source_cur.execute(f"""SELECT flight_date, COUNT(*) FROM flight_data WHERE TO_CHAR(flight_date, 'YYYY-MM-DD') = '{date}' GROUP BY flight_date""")
        results     = source_cur.fetchone()
    except psql_connector.Error as err:
        print(err)
                
    try:
        target_conn = psql_connector.connect(**db_config['target'])
        target_cur  = target_conn.cursor()
        target_cur.execute("INSERT INTO flight_data_summary(flight_date, flight_count)\
                                VALUES(%s, %s)", results)
        target_conn.commit()
    except psql_connector.Error as err:
        print(err)
        
    target_cur.close()
    target_conn.close()
    source_cur.close()
    source_conn.close()


default_args = {
    'owner'           : 'Albiyan',
    "depends_on_past" : False,
    'start_date'      : datetime(2019, 5, 4),
    'end_date'        : datetime(2019, 5, 8),
    'email'           : 'abdikaalbiyan@gmail.com',
    'email_on_failure': False,
    'email_on_retry'  : False,
    'retries'         : 1,
    'retry_delay'     : timedelta(minutes=1)
}

dag = models.DAG(
    'ETL_Flight_Dataset',
    default_args      = default_args,
    description       = 'ETL_Flight_Dataset',
    schedule_interval = '0 1 * * *',
)

insert_data_json_to_source_db_task = PythonOperator(
    task_id         = 'insert_data_json_to_source_db',
    provide_context = True,
    python_callable = insert_data_json_to_source_db,
    op_kwargs       = {"date" : '{{ds}}'},
    dag             = dag,
)

extract_transform_load_task = PythonOperator(
    task_id         = 'extract_transform_load',
    provide_context = True,
    python_callable = extract_transform_load,
    op_kwargs       = {"date" : str('{{ds}}')},
    dag             = dag,
)

insert_data_json_to_source_db_task >> extract_transform_load_task