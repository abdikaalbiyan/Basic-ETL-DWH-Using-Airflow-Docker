# Basic-ETL-DWH-Using-Airflow-Docker


## Flow
<p align="center">
    <img width="720" alt="Screen Shot 2021-11-18 at 22 45 38" src="https://user-images.githubusercontent.com/22974798/142448422-991209f4-e6b9-438c-8254-faf8b0198e9d.png">
</p>

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
mkdir ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
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

Open [http://localhost:5884](http://localhost:5884) to access The UI of Apache Airflow Webserver.<br>
> Username: airflow<br>
> Password: airflow<br>

<br><br>

## Result

<p align="center">
    <img width="1431" alt="Screen Shot 2021-11-18 at 21 35 31" src="https://user-images.githubusercontent.com/22974798/142442005-62a67954-c874-4ed1-8f04-2617a3ec9f14.png">
<i>Airflow home UI</i>
</p><br>


<p align="center">
    <img width="1160" alt="Screen Shot 2021-11-18 at 21 34 37" src="https://user-images.githubusercontent.com/22974798/142442338-1b89014b-e21d-4aca-9921-11f3b8485f90.png">
<i>JSON data that has been imported to Source DB</i>
</p><br>


<p align="center">
    <img width="314" alt="Screen Shot 2021-11-18 at 21 35 01" src="https://user-images.githubusercontent.com/22974798/142442787-4127e3b2-0072-4916-b432-3b4ebb50a5fe.png">
    
<i>The results from Python on Airflow batch processing</i>
    
</p><br>
