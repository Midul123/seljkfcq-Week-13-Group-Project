# 👾 Terraform scripts for easy AWS resource creation/deletion

These files contain all that is needed to set up our AWS resources on the cloud.

## ⚠️ The following resources were created in AWS UI and therefore will need to be setup manually

- 

## 🔨 Setup

Make sure to add a `terraform.tfvars` file with your AWS access key and secret access key in this format:
```
AWS_ACCESS_KEY = [your_access_key]
AWS_SECRET_KEY = [your_secret_key]
```

You'll also need to add your password to access the database, in this format:
```
DB_PASSWORD = [your_db_password]
```

## 🚀 How to run

- If it's the first time, run `terraform init`.
- To create resources, run `terraform apply`.
- When you're done, run `terraform destroy`.