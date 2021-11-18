# Basic-ETL-DWH-Using-Airflow-Docker

## Prequisite
- Python 3.8.3
- Docker

## Initializing Source DB Environment
Run:
```bat
cd Basic-ETL-DWH-Using-Airflow-Docker/Source
docker-compose up -d
```
That command will build PostgreSql inside Docker Container and create '''flight_data''' table inside the database.<br>
Then run
```bat
docker inspect <container id> | grep "Gateway"
```
To get the Source DB's Host.<br>
The Source DB is ready to use.


## Initializing Target DB Environment
Run:
```bat
cd Basic-ETL-DWH-Using-Airflow-Docker/Destination
docker-compose up -d
```
That command will build PostgreSql inside Docker Container and create ''flight_data_summary''' table inside the database.<br>
Then run
```bat
docker inspect <container id> | grep "Gateway"
```
To get the Target DB's Host.<br>
The Target DB is ready to use.



## Initializing Airflow Environment
```bat
cd Basic-ETL-DWH-Using-Airflow-Docker/Airflow
docker-compose up airflow-init
docker-compose up
```

