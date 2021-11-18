# Basic-ETL-DWH-Using-Airflow-Docker

## Prequisite
- Python 3.8.3
- Docker v20.10.5


## Installation

Use git to clone this repository

```bat 
git clone https://github.com/abdikaalbiyan/Basic-ETL-DWH-Using-Airflow-Docker.git
```


### Initializing Source DB Environment

Run:
```bat
cd Basic-ETL-DWH-Using-Airflow-Docker/Source
docker-compose up -d
```
That command will build PostgreSql inside Docker Container and create ``flight_data`` table inside the database.<br>
Then run this to get the Source DB's host to be input into the config file later<br>
```bat
docker inspect <container id> | grep "Gateway"
```
The Source DB is ready to use.<br><br>


### Initializing Target DB Environment
Run:
```bat
cd Basic-ETL-DWH-Using-Airflow-Docker/Destination
docker-compose up -d
```
That command will build PostgreSql inside Docker Container and create ``flight_data_summary`` table inside the database.<br>
Then run this to get the Target DB's host to be input into the config file later<br>
```bat
docker inspect <container id> | grep "Gateway"
```
The Target DB is ready to use.<br><br>



### Initializing Airflow Environment
```bat
cd Basic-ETL-DWH-Using-Airflow-Docker/Airflow
docker-compose up airflow-init
```

Edit ./config.py to change Host Address for every DB according to your machine
```python
db_config = {
    'source' : {
                "host"      : "172.22.0.1", #Get your host from $docker inspect <container id> | grep "Gateway"
                "user"      : "postgres",
                "password"  : "postgres",
                "port"      : '5434',
                "database"  : "postgres"},
    'target' : {
                "host"      : "172.24.0.1", #Get your host from $docker inspect <container id> | grep "Gateway"
                "user"      : "postgres",
                "password"  : "postgres",
                "port"      : '5435',
                "database"  : "postgres"}
    }

#edit your Docker Container Dir here
source_dir = '/opt/airflow/dags/json-files'
```

Then run:
```bat
docker-compose up
```

Open [http://localhost:5884](http://localhost:5884) to access The UI of Apache Airflow Webserver.<br><br>

## Result