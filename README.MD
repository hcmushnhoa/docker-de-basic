docker network create pg-network
#docker run postgres
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "D:/Download from Edge/docker/docker_sql_data":/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:17
# run pgadmin4 with network 
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
# run pgadmin4
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4

# running locally
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"


# in python,run ingest.py  with argument ... 
python ingest.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=ny_taxi_data \
  --url=${URL}

#Build image docker and running to ingest data (connect container to network )


docker build -t taxi_data:v001 .
#(new url with ipv4)
URL="https://192.168.2.45:8000/yellow_tripdata_2024-01.parquet"
docker run -it \
  --network=pg-network \
  taxi_data:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=ny_taxi_data \
    --url=${URL}
#run docker compose
docker compose up
docker compose down #to shutting down compose
#and can run it in background with detached mode
docker compose up -d
 
