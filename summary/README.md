# 🧰 Pipeline

This folder contains all the files to run the summarising of the RDS data and the push to long-term storage.

## 🗂️ Files explained

- `README.md`
    - The file that you're currently reading
- `utils.py`
    - Contains utility functions being used in the other files
- `parquet_files.py`
    - Gets the data stored in the RDS, summarises it, pushes it to a dedicated S3 bucket as partitioned parquet files and finally deletes the data from the RDS
- `dockerfile`
    - Dockerises the files
- `requirements.txt`
    - All requirements needed to run the files

## 🛠️ Setup

Run the following commands to be able to connect to `pyodbc`:

1. `brew install unixodbc`
2. `brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release`
3. `brew install msodbcsql18 mssql-tools18`

Also make sure to add a `.env` file in this directory with the following information:

```
DB_HOST=c19-plants-db.c57vkec7dkkx.eu-west-2.rds.amazonaws.com
DB_PORT=1433
DB_USER=gamma
DB_PASSWORD=[your_db_password]
DB_NAME=plants
DB_DRIVER=ODBC Driver 18 for SQL Server
```

## 🚀 How to run

1. Follow the instructions in the `terraform` folder to set up all necessary resources in AWS.
2. Back in this folder, run the following commands in order to authenticate with AWS, dockerise, tag, and push the image to the right ECR repository:
    - `aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin [YOUR_AWS_ACCOUNT_ID].dkr.ecr.eu-west-2.amazonaws.com`
    - `docker buildx build -t [IMAGE_NAME]:latest --platform "Linux/amd64" --provenance=false .`
    - `docker tag [IMAGE_NAME]:latest [YOUR_AWS_ACCOUNT_ID].dkr.ecr.eu-west-2.amazonaws.com/c19-seljkfcq-ecr-tf-2:latest`
    - `docker push [YOUR_AWS_ACCOUNT_ID].dkr.ecr.eu-west-2.amazonaws.com/c19-seljkfcq-ecr-tf-2:latest`

The AWS Lambda associated to that ECR will then start triggering automatically every 24 hours, pulling the data from the RDS, summarising it, pushing it to the S3 bucket and deleting everything from the RDS at the end so it's ready for the new daily data.