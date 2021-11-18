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