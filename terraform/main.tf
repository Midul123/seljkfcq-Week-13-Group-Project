## S3 bucket
resource "aws_s3_bucket" "project-s3" {
  bucket = "c19-seljkfcq-project"

  force_destroy = true
}


## ECR repository
resource "aws_ecr_repository" "project-ecr" {
  name                 = "c19-seljkfcq-ecr-tf"
  image_tag_mutability = "MUTABLE"
}


## Lambda and AWS role

# Role
resource "aws_iam_role" "lambda_exec_role" {
 name = "seljkfcq-lambda-execution-role"
  assume_role_policy = jsonencode({
   Version = "2012-10-17",
   Statement = [
     {
       Action = "sts:AssumeRole",
       Principal = {
         Service = "lambda.amazonaws.com"
       },
       Effect = "Allow"
     }
   ]
  })
}
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
 role       = aws_iam_role.lambda_exec_role.name
 policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# # Cloudwatch log group
# resource "aws_cloudwatch_log_group" "example" {
#   name              = "/aws/lambda/c19-seljkfcq-lambda-function-tf"
#   retention_in_days = 14

#   tags = {
#     Environment = "production"
#     Application = "project-lambda-1"
#   }
# }

# Lambda
resource "aws_lambda_function" "project-lambda-1" {
  function_name = "c19-seljkfcq-lambda-function-tf"
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"
  image_uri     = var.IMAGE_URI
  memory_size = 512
  timeout     = 300
  logging_config {
    log_format            = "JSON"
    application_log_level = "INFO"
    system_log_level      = "WARN"
  }

  #depends_on = [aws_cloudwatch_log_group.example]

  environment {
    variables = {
      DB_HOST=var.DB_HOST
      DB_PORT=1433
      DB_USER=var.DB_USER
      DB_PASSWORD=var.DB_PASSWORD
      DB_NAME=var.DB_NAME
      DB_SCHEMA=var.DB_SCHEMA
      DB_DRIVER=var.DB_DRIVER
    }
  }

  architectures = ["x86_64"]
}

## Scheduler 1
resource "aws_iam_role" "scheduler_lambda" {
  name = "m3y-scheduler-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
        {
          Action = "sts:AssumeRole"
          Principal = {
            Service = "scheduler.amazonaws.com"
          },
          Effect = "Allow"
        }
   ]
  })
}
resource "aws_iam_role_policy_attachment" "scheduler_lambda" {
  role       = aws_iam_role.scheduler_lambda.name
  policy_arn = aws_iam_policy.scheduler_lambda.arn
}
resource "aws_iam_policy" "scheduler_lambda" {
  name = "m3y-Scheduler-Lambda-Policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Action" : [
          "lambda:InvokeFunction"
        ],
        Effect   = "Allow"
        Resource = aws_lambda_function.project-lambda-1.arn
      },
    ]
  })
}

# Scheduler
resource "aws_scheduler_schedule" "lambda-1-scheduler" {
  name = "c19-m3y-trigger-lambda-scheduler-minute"
  group_name = "default"
  schedule_expression = "cron(* * * * ? *)"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn = aws_lambda_function.project-lambda-1.arn
    role_arn = aws_iam_role.scheduler_lambda.arn
  }
}