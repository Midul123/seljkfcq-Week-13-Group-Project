# 👾 Terraform scripts for easy AWS resource creation/deletion

These files contain all that is needed to set up our AWS resources on the cloud.

## 🛠️ Setup

Make sure to add a `terraform.tfvars` file with your AWS access key and secret access key in this format:
```
AWS_ACCESS_KEY = [your_access_key]
AWS_SECRET_KEY = [your_secret_key]
```

You'll also need to add your password to access the database, and the ARN of the role created for the Lambda function, in this format:
```
DB_PASSWORD = [your_db_password]
IAM_USER_ARN=[your_personal_aws_user_arn]
```

## 🚀 How to run

- If it's the first time, run `terraform init`.
- To create resources, run `terraform apply`.
- When you're done, run `terraform destroy`.