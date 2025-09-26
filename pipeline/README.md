# 🧰 Pipeline

This folder contains all the files to run our ETL pipeline.

## 🗂️ Files and folders explained

Files:

- `README.md`
    - The file that you're currently reading
- `utils.py`
    - Contains utility functions being used in the other files
- `extract.py`
    - Gets the plant data from the API endpoint and stores all not-null results in a JSON file
- `transform.py`
    - Cleans the data in the JSON file and outputs it to a CSV file
- `load.py`
    - Uploads plant data to a Microsoft SQL server database
- `pipeline.py`
    - Performs the whole ETL process
- `test_pipeline.py`
    - Tests functions in `pipeline.py`
- `schema.sql`
    - Contain all code required to create our database tables and relationships
- `connect.sh`
    - Script to connect to the database from the command line
- `reset.sh`
    - Script to reset the database from the command line
- `dockerfile`
    - File to dockerise the pipeline
- `requirements.txt`
    - All requirements needed to run the pipeline

Folders:

- `notebooks/`
    - Notebooks used for experiments throughout the development

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
    - `docker tag [IMAGE_NAME]:latest [YOUR_AWS_ACCOUNT_ID].dkr.ecr.eu-west-2.amazonaws.com/c19-seljkfcq-ecr-tf:latest`
    - `docker push [YOUR_AWS_ACCOUNT_ID].dkr.ecr.eu-west-2.amazonaws.com/c19-seljkfcq-ecr-tf:latest`

The AWS Lambda associated to that ECR will then start triggering automatically every minute, pushing data about each plant to the RDS.