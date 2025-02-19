# Configuration Guide
1. Ensure that a PostgreSQL environment is available, or set it up using Docker:
    ```
    docker run -d \
      --name postgres \
      -e POSTGRES_USER= \
      -e POSTGRES_PASSWORD= \
      -e POSTGRES_DB=delta \
      -p 5432:5432 \
      -v ~/postgres_data:/var/lib/postgresql/data \
      postgres
    ```
2. run
   ```
   git clone https://github.com/hyolics/delta.git ./airflow
   ```
3. Place the Kaggle API token in ./kaggle and the PostgreSQL connection information in /dags/.env.
4. run
   ```
   cd /airflow
   docker-compose up -d
   ```
5. Based on the docker-compose.yml configuration, Airflow will automatically initialize, download the required packages from requirements.txt, and automatically recognize etl_pipeline.py and elt_pipeline.py as two DAGs.
6. Check Airflow UI: http://localhost:8080 (airflow/airflow)
         Grafana UI: http://localhost:3000
7. Set up the connection in Airflow UI(connections) and Grafana UI(data source).
8. Import grafana.json to Grafana UI to set up dashboard.

