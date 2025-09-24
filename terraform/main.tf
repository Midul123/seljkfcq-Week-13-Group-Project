
resource "aws_s3_bucket" "project-s3" {
    bucket = "c19-seljkfcq-project"

    force_destroy = true
}




















resource "aws_ecr_repository" "project-ecr" {
  name                 = "c19-seljkfcq-ecr-tf"
  image_tag_mutability = "MUTABLE"
}