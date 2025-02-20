Tools: 
- DB: postgresSQL
- Airflow
- Dashboard: Grafana
- Python packages: python-dotenv, sqlalchemy, apache-airflow, pandas, Kaggle, datetime

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

* If you don't want to use Airflow to run it, you can achieve the same goal by directly using ./modules/etl/main.py and ./modules/elt/main.py.

# Demo
## Dashboard
![image](https://github.com/user-attachments/assets/e927033e-eabe-4871-9032-3f6b2f8bb832)
![image](https://github.com/user-attachments/assets/4c6f0cc1-6147-4dc9-aa1d-61ba9c773fc1)
## PostgreSQL
### ETL
![image](https://github.com/user-attachments/assets/8018ea2d-40f1-430a-9d1b-a916b91b9812)
* demo_data: https://drive.google.com/drive/folders/1BzkuzcgglVufgT7JW8DXQVpoaJ6lpLkX?usp=drive_link
### ELT
![image](https://github.com/user-attachments/assets/5a4e97ff-d09c-4a46-a0bf-e9641f6e1b66)










