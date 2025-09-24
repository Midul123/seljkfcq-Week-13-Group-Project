variable "AWS_REGION" {
  type = string
  default = "eu-west-2"
}

variable "AWS_ACCESS_KEY" {
  type = string
}

variable "AWS_SECRET_KEY" {
  type = string
}

variable "DB_HOST" {
  type = string
  default = "c19-plants-db.c57vkec7dkkx.eu-west-2.rds.amazonaws.com"
}

variable "DB_PORT" {
  default = "1443"
}

variable "DB_NAME" {
  type = string
  default = "plants"
}
variable "DB_USER" {
  type = string
  default = "gamma"
}
variable "DB_SCHEMA" {
  type = string
  default = "gamma"
}

variable "DB_PASSWORD" {
  type = string
}

variable "DB_DRIVER" {
  type = string
  default = "ODBC Driver 18 for SQL Server"
}

variable "IMAGE_URI" {
  type = string
  default = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c19-seljkfcq-ecr-tf:latest"
}