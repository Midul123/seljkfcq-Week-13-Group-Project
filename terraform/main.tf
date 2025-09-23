
resource "aws_s3_bucket" "project-s3" {
    bucket = "c19-seljkfcq-project"

    force_destroy = true
}