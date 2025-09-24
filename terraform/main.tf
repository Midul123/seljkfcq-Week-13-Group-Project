
resource "aws_s3_bucket" "project-s3" {
    bucket = "c19-seljkfcq-project"

    force_destroy = true
}

resource "aws_lambda_function" "project-lambda-1" {
  function_name = "c19_seljkfcq-lambda_function-tf"
  role          = "insert role:arn"
  package_type  = "Image"
  image_uri     = "Insert"
  memory_size = 512
  timeout     = 300

  architectures = ["x86_64"]
}